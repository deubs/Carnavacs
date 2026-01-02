#!/usr/bin/python
#--------------------------------------
#  molinete_system_v1.py 
#  Author: Emiliano Melchiori
#  Date: 28/11/2024
#  OrangePI Zero3 access control system
#  based on GM65 bar code scanner, NexuPOS Jet 111 bar code scanner, 16x2 LCD i2c, API calls 

import serial
import LCDI2C
import threading
import queue
import time
import checklan
from requests import post, exceptions, Session
from datetime import datetime, date
from apikeys import keys
from evdev import InputDevice, categorize, ecodes, list_devices
import calendar
import platform
# import pdb
from os import makedirs
from os.path import exists, join
from json import dumps
import logging
import logging.handlers
import structlog
import sys
import random

if "tango" in platform.node():
    import wiringpi
    print("importing wiringpi")
    GPIO_RESTART = 9 #PC15
    GPIO_RELAY_OUT = 10 #PC14
    GPIO_INPUT_1 = 13   #PC7
    workingdir = "/home/orangepi/"
else:
    from gpiozero import Button, DigitalInputDevice, OutputDevice
    print("importing gpiozero")
    rasp_button_restart = Button(4, pull_up=True) # PIN 7
    rasp_relay_out = OutputDevice(17) # PIN 11
    rasp_sensor_in = DigitalInputDevice(27) # PIN 11
    workingdir = "/home/pi/"

structlog.contextvars.bind_contextvars(
    device=platform.node(),
)

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars, 
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logging.basicConfig(
    filename= f"{workingdir}/logs/{platform.node()}.log",
    filemode='a',
    format="%(message)s",
    #stream=sys.stdout,
    level=logging.INFO,
)

#disable unstructured log
logging.getLogger('asyncio').setLevel(logging.WARNING)

logger = structlog.get_logger()


# STATUS VARS
BLAN = False
BGM65 = False
# ORANGE PI ZERO 3 WIRING

apiurlb = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurl = "http://192.168.40.100/Ticket/Validate"

# threading_event = threading.Event()
# scancodes = {
# 	11:	u'0',
# 	2:	u'1',
# 	3:	u'2',
# 	4:	u'3',
# 	5:	u'4',
# 	6:	u'5',
# 	7:	u'6',
# 	8:	u'7',
# 	9:	u'8',
# 	10:	u'9'
# }

scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

idev = None
sp = None

NOT_RECOGNIZED_KEY = u'X'
l1 = LCDI2C.LCD_LINE_1
l2 = LCDI2C.LCD_LINE_2

class PauseDeviceTOKEN:
    def __init__(self):
        self.is_paused = False
    
    def pauseDevice(self):
        self.is_paused = True
    
    def resumeDevice(self):
        self.is_paused = False


pauseDevice = PauseDeviceTOKEN()

logger.info(
        "device_status",
        workingdir=workingdir,
        scancodes=scancodes,
        network_status="online",
)


def detectInputDevice():
    """
        From a list of input devices, select the one that matches the filter
    """
    devices = [InputDevice(path) for path in list_devices()]
    inputdev = None
    print(devices)
    for device in devices:
        print(device.name)
        if ("IMAGER 2D" in device.name) or \
            ("BF SCAN SCAN KEYBOARD" in device.name) or \
                ("NT USB Keyboard" in device.name) or \
                    ("TMS HIDKeyBoard" in device.name) or \
                        ("ZKRFID R400" in device.name):

            inputdev = device.path
            break
    return inputdev
    

def connectInputDevice(inputdev):
    try:           
        device = InputDevice(inputdev) # Replace with your device
    except Exception as e:
        print(e)
        return None
    else:
        print(device)
        print(device.capabilities())
        return device


def readBarCodes(device, q: queue, pause: PauseDeviceTOKEN):
    barcode = ''
    while True:
        try:
            for event in device.read_loop():
                if not pause.is_paused:
                    if event.type == ecodes.EV_KEY:
                        eventdata = categorize(event)
                        if eventdata.keystate == 1: # Keydown
                            scancode = eventdata.scancode
                            # print(scancode)
                            if scancode == 28: # Enter
                                q.put(barcode)
                                barcode = ''
                            else:
                                # key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                                # if scancode > 48 and scancode < 128:
                                # key = str(scancode)
                                key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                                barcode = barcode + key
                                # else: 
                                    # key = NOT_RECOGNIZED_KEY
                                    # print('unknown key, scancode=' + str(scancode))
        except Exception as e:
            print(e)
            idev = None
            exit()


def readPort(serialP, q:queue, pause: PauseDeviceTOKEN):
    """
        Serial port communication with GM65 barcode reader
    """
    print("Serial Port Opened")
    breading = True
    bcode = True
    if serialP.isOpen():
        while breading:
            print("Reading Serial Port")
            data = ""
            bcode = True
            if not pause.is_paused:
                while bcode:
                    if q.empty():
                        cmdRet = serialP.read().decode()
                        if (cmdRet == '\r' or cmdRet == '\n'):
                            q.put(data)
                            bcode = False
                        else:
                            data += str(cmdRet)
    else:
        print("Port is Closed")


def initSerialPort():
    """
        Initiates serial port in OPIz3
        Serial port is UART5 in OPIz3.
    """
    serial_port = None
    try:
        serial_port = serial.Serial(
            port="/dev/ttyS5",
            timeout=None,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        print("connected to: " + serial_port.portstr)
    except Exception as e:
        print(e)
    return serial_port

bGATEOPEN = False

def ISRSignal(iplatform):
    """
        
    """
    print("Reading inductive...")
    bGATEOPEN = False
    bwait4Hole = True
    print("State is HIGH...")
    if iplatform == 1:
        print("waiting hole")
        while bwait4Hole:
            bwait4Hole = wiringpi.digitalRead(GPIO_INPUT_1)
    else:
        while bwait4Hole:
            bwait4Hole = rasp_sensor_in.pin.state
    print("State is LOW")
    return bwait4Hole


def initGPIO():
    """
        Initiates GPIO. Only for OrangePI Zero 3
        OPIz3 using GPIO 17 and 18 for relays and 19 for inductive sensors.
    """
    print("INIT GPIO")
    try:
        if "tango" in platform.node():
            print("init wiringpi")
            wiringpi.wiringPiSetup()
            wiringpi.pinMode(GPIO_RELAY_OUT, wiringpi.GPIO.OUTPUT)
            wiringpi.digitalWrite(GPIO_RELAY_OUT, wiringpi.GPIO.LOW)
            wiringpi.pinMode(GPIO_INPUT_1, wiringpi.GPIO.INPUT)
            wiringpi.pinMode(GPIO_RESTART, wiringpi.GPIO.INPUT)
            wiringpi.pullUpDnControl(GPIO_INPUT_1, wiringpi.GPIO.PUD_UP)
            wiringpi.pullUpDnControl(GPIO_RESTART, wiringpi.GPIO.PUD_UP)
    except Exception as e:
        print(e)


def enableGate():
    """
    Dissable COIL using relays. Iluminate GREEN light 
    Wait until signal from inductive sensor
    Enable COIL releasing relays. Iluminate RED light
    """
    if "tango" in platform.node():
        print("Release RELAYS")
        logmessage('info', 'Release RELAYS')
        wiringpi.digitalWrite(GPIO_RELAY_OUT, wiringpi.GPIO.HIGH)
        if "tango14" in platform.node() or "vehiculos" in platform.node():
            time.sleep(2)
            bHole = False
        else:
            bHole = ISRSignal(1)
        if not bHole:
            print("Activate RELAYS")
            logmessage('info', 'ACTIVATE RELAYS')
            wiringpi.digitalWrite(GPIO_RELAY_OUT, wiringpi.GPIO.LOW)
            return True
        return False
    else:
        if "baliza" in platform.node() or "vehiculos" in platform.node():
            # raspberry box delay for commute from ON to OFF
            logmessage('info', 'RELEASE RELAYS')
            rasp_relay_out.on()
            time.sleep(1)
            rasp_relay_out.off()
            logmessage('info', 'ACTIVATE RELAYS')
            return True
        else:
            print("release RELAY")
            logmessage('info', 'RELEASE RELAYS')
            rasp_relay_out.on()            
            bHole = ISRSignal(0)
            if not bHole:
                logmessage('info', 'ACTIVATE RELAYS')
                print("Activate RELAYS")
                rasp_relay_out.off()
                return True
            return False


def printSTATUS(lcd):
    lcd.lcd_string("LAN " + str(BLAN), l1)
    lcd.lcd_string("GM65 " + str(BGM65) + " JET: " + str(BJET), l2)
    time.sleep(5)
    lcd.lcd_string("MAC: ", l1)
    lcd.lcd_string(checklan.hexMAX, l2)
    time.sleep(5)
    lcd.lcd_string("IP: ", l1)
    lcd.lcd_string(checklan.ipADDRESS, l2)


def processResponse(response):
    apistatus = response['success']
    isValid = response['result']['isValid']
    m1 = response['result']['m1']
    m2 = response['result']['m2']
    return {'apistatus': apistatus, 'code': isValid, 'm1': m1, 'm2': m2}


def apicall(code):
    """

    """
    apikey = keys['key1']
    header = {
        'X-API-Key': f'{apikey}',
        'Content-Type': "application/json"
    }
    payload = {'code': code}
    try:
        response = post(apiurl, params=payload, headers=header, timeout=3)
        if response.status_code == 200:
            return processResponse(response.json())
        if response.status_code == 401:
            print(response.status_code)
        if response.status_code == 404:
            print(response.status_code)
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'} 
    except exceptions.Timeout:
        print("The request timed out!")
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}
    except Exception as e:
        print(e)
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}

BINITLCD = False
def initLCD():
    lcd = None
    try:
        lcd = LCDI2C.LCD()
        lcd.lcd_init()
        lcd.lcd_string("LCD INIT", l1)
        lcd.lcd_string(platform.node(), l2)
        logmessage('info', 'LCD INIT')
        time.sleep(2)
        BINITLCD = True
    except Exception as e:
        logmessage('critical', 'LCD DID NOT INIT')
        BINITLCD = False
    return lcd


def createFile():
    """
    Creates log file for read codes
    """
    fdir = join(workingdir, 'tickets')
    if not exists(fdir):
        makedirs(fdir)
    f = None
    dt = date.today().isoformat()
    try:
        fname = join(fdir, f'tickets_{dt}.txt')
        f = open(fname, "a")
    except Exception as e:
        logmessage('critical', e)
    return f


def logmessage(level, message):
    """
    logs messages to file
    """
    log = getattr(logger, level)
    log(message)

def initInputDevice(queue):
    """
    """
    idev = detectInputDevice()
    if idev is not None:
        dev = connectInputDevice(idev)
        threading.Thread(target = readBarCodes, args = (dev, queue, pauseDevice, ), daemon = True).start()
        logmessage('info', 'INPUT DEVICE THREAD CREATED')
    return idev


def initSerialDevice(queue):
    """
    """
    sp = initSerialPort()
    if sp != None:
        threading.Thread(target = readPort, args = (sp, queue, pauseDevice, ) , daemon = True).start()
        BGM65 = True
        time.sleep(2)
    return sp

import os
def checkCode(code:str, lcd):
    """
        Reboot and Shutdown codes
    """
    if code == '00000000000100000000000':
        logmessage('info', 'REBOOT REQUIRED BY QR')
        lcd.lcd_string("REBOOT BY QR", l1)
        lcd.lcd_string("REBOOT BY QR", l2)
        os.system('reboot')
        time.sleep(5)
    if code == "11111111111111111111111":
        logmessage('info', 'SHUT DOWN REQUIRED BY QR')
        lcd.lcd_string("SHUTDOWN BY QR", l1)
        lcd.lcd_string("SHUTDOWN BY QR", l2)
        os.system('systemctl poweroff')
        time.sleep(5)

def main():
    """
        Main function
    """
    lcd = initLCD()
    if lcd is not None:
        logmessage('info', 'LCD init')
    fhandler = createFile()

    BLAN, ip = checklan.checkLAN(checklan.target, checklan.timeout)
    if BLAN:
        lcd.lcd_string("LAN DETECTED", l1)
        lcd.lcd_string(ip, l2)
        logmessage('info', f'LAN DETECTED {ip}')
        time.sleep(2)
    else:
        lcd.lcd_string("LAN NOT DETECTED", l1)
        logmessage('error', f'LAN NOT DETECTED')
        time.sleep(2)

    jet111q = queue.Queue(maxsize = 1)
    
    initGPIO()
    # if not bgpio:
    #     logmessage('critical', 'GPIO NOT INITIATED')
    #     logmessage('critical', 'SYSTEM WILL EXIT NOW')
    #     lcd.lcd_string("PROBLEMA GPIO", l1)
    #     lcd.lcd_string("REINICIO SISTEMA", l2)
    #     time.sleep(2)
    #     exit()

    idev = initInputDevice(jet111q)
    if idev is not None:
        lcd.lcd_string("INPUT DEV ON", l2)
        logmessage('info', "INPUT DEV ON")
    else:
        lcd.lcd_string("INPUT DEV OFF", l2)
        logmessage('error', "INPUT DEV OFF")
        
    time.sleep(1)
    
    if "raspi" in platform.node() or "vehiculo" in platform.node():
        sp = None
    else:
        gm65q = queue.Queue(maxsize = 1)
        sp = initSerialDevice(gm65q)

    nthreads = threading.enumerate()
    code = None
    while True:
        gm65data = None
        jet111data = None
        marked = False
        brestart = 1
        if "tango" in platform.node():
            brestart = wiringpi.digitalRead(GPIO_RESTART)
        else:
            brestart = rasp_button_restart.pin.state

        if nthreads != threading.enumerate():
            logmessage('critical', 'INPUT DEVICE IS OFF. INFORM')
            lcd.lcd_string("PISTOLA", l1)
            lcd.lcd_string("DESCONECTADA", l2)
            time.sleep(2)
            brestart = 0

        if brestart == 0:
            lcd.lcd_string("REINICIANDO", l1)
            lcd.lcd_string("YA VOLVEMOS", l2)
            logmessage('critical', 'RESTART REQUIRED')
            if fhandler is not None:
                fhandler.close()
            exit()

        if code is None:
            FAILURE_COUNT = 5
            if sp is not None:
                if not gm65q.empty():
                    gm65data = gm65q.get()
                    if gm65data is not None:
                        # lcd.lcd_string(gm65data, l1)     
                        logmessage('info', f'{gm65data}')
                        code = gm65data
            if idev is not None:
                if not jet111q.empty():
                    jet111data = jet111q.get()
                    if jet111data is not None:
                        # lcd.lcd_string(jet111data, l1)     
                        logmessage('info', f'jet data {jet111data}')
                        code = jet111data
            else:
                lcd.lcd_string("PISTOLA", l1)
                lcd.lcd_string("DESCONECTADA", l2)
                time.sleep(2)

        bfinalize_job = False
        if (code is not None):
            checkCode(code, lcd)
            pauseDevice.pauseDevice()
            result = apicall(code)
            logmessage('info', dumps(result))
            if result['apistatus'] == True:
                lcd.lcd_string(result['m1'], l1)
                lcd.lcd_string(result['m2'], l2)
                if result['code'] == False:
                    logmessage('error', f"{code} {result['m1']} {result['m2']}")
                    time.sleep(1)
                else:
                    logmessage('info', f"{code} {result['m1']} {result['m2']}")
                    marked = enableGate()
                    if marked:
                        logmessage('info', f'{code} marked')
                ticket_string = f'code: {code}, status:{result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
                bfinalize_job = True
            else:
                logmessage('critical', f'FALLA DE SISTEMA - REINTENTANDO')
                lcd.lcd_string("FALLA DE SISTEMA", l1)
                lcd.lcd_string("REINTENTANDO", l2)
                FAILURE_COUNT -= 1
                ticket_string = f'code: {code}, status: api failed, timestamp: {datetime.now()} \n'
                if FAILURE_COUNT == 0:
                    logmessage('critical', f'FALLA PERMANENTE - INFORME PROBLEMA')
                    lcd.lcd_string("FALLA PERMANENTE", l1)
                    lcd.lcd_string("INFORME PROBLEMA", l2)
                    time.sleep(3)
                    ticket_string = f'code: {code}, status: api failed permanent, timestamp: {datetime.now()} \n'
                    bfinalize_job = True
                    
            if bfinalize_job:
                code = None
                pauseDevice.resumeDevice()
            if fhandler is not None:
                fhandler.write(ticket_string)
                fhandler.flush()    
        else:
            code = None
            lcd.lcd_string("CARNAVAL 2026", l1)
            lcd.lcd_string("NUEVO INGRESO", l2)
            

if __name__ == '__main__':
    main()
