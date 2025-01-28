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

logging.basicConfig(filename= f"/home/pi/logs/{platform.node()} - {datetime.today()}",
                    filemode='a',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('Synchronous Logging')


if "tango" in platform.node() or "vehiculos" in platform.node():
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

print(workingdir)

# STATUS VARS
BLAN = False
BGM65 = False
BJET = False
# ORANGE PI ZERO 3 WIRING

apiurlb = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurl = "http://192.168.40.100/Ticket/Validate"

# threading_event = threading.Event()
scancodes = {
	11:	u'0',
	2:	u'1',
	3:	u'2',
	4:	u'3',
	5:	u'4',
	6:	u'5',
	7:	u'6',
	8:	u'7',
	9:	u'8',
	10:	u'9'
}

idev = None
sp = None

print(scancodes)
NOT_RECOGNIZED_KEY = u'X'

class PauseDeviceTOKEN:
    def __init__(self):
        self.is_paused = False
    
    def pauseDevice(self):
        self.is_paused = True
    
    def resumeDevice(self):
        self.is_paused = False


pauseDevice = PauseDeviceTOKEN()


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
    print('begin reading...')
    barcode = ''
    while True:
        try:
            for event in device.read_loop():
                if not pause.is_paused:
                    if event.type == ecodes.EV_KEY:
                        eventdata = categorize(event)
                        if eventdata.keystate == 1: # Keydown
                            scancode = eventdata.scancode
                            if scancode == 28: # Enter
                                print("putting in queue")
                                q.put(barcode)
                                barcode = ''
                            else:
                                key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                                barcode = barcode + key
                                if key == NOT_RECOGNIZED_KEY:
                                    print('unknown key, scancode=' + str(scancode))
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
        if "tango" in platform.node() or "vehiculos" in platform.node():
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
    if "tango" in platform.node() or "vehiculos" in platform.node():
        print("Release RELAYS")
        wiringpi.digitalWrite(GPIO_RELAY_OUT, wiringpi.GPIO.HIGH)
        if "tango14" == platform.node() or "vehiculos" in platform.node():
            time.sleep(2)
            bHole = False
        else:
            bHole = ISRSignal(1)
        if not bHole:
            print("Activate RELAYS")
            wiringpi.digitalWrite(GPIO_RELAY_OUT, wiringpi.GPIO.LOW)
            return True
        return False
    else:
        if "baliza" in platform.node() or "raspidiscabaliza" in platform.node():
            # raspberry box delay for commute from ON to OFF
            rasp_relay_out.on()
            time.sleep(2)
            rasp_relay_out.off()
            return True
        else:
            print("release RELAY")
            rasp_relay_out.on()            
            bHole = ISRSignal(0)
            if not bHole:
                print("Activate RELAYS")
                rasp_relay_out.off()
                return True
            return False


def printSTATUS(lcd):
    lcd.lcd_string("LAN " + str(BLAN), LCDI2C.LCD_LINE_1)
    lcd.lcd_string("GM65 " + str(BGM65) + " JET: " + str(BJET), LCDI2C.LCD_LINE_2)
    time.sleep(5)
    lcd.lcd_string("MAC: ", LCDI2C.LCD_LINE_1)
    lcd.lcd_string(checklan.hexMAX, LCDI2C.LCD_LINE_2)
    time.sleep(5)
    lcd.lcd_string("IP: ", LCDI2C.LCD_LINE_1)
    lcd.lcd_string(checklan.ipADDRESS, LCDI2C.LCD_LINE_2)


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
        printMessage(lcd, "LCD INIT", LCDI2C.LCD_LINE_1, True)
        printMessage(lcd, platform.node(), LCDI2C.LCD_LINE_2, True)
        time.sleep(2)
        BINITLCD = True
    except Exception as e:
        print(e)
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
        print(e)
    return f


import pdb
def printMessageDict(lcd_object, messagedict):
    print(messagedict)
    pdb.set_trace()
    try:
        for line, message in messagedict:
            print(line, message)
            lcd_object.lcd_string(message, line)
    except Exception as e:
        logmessage('error', e)


def printMessage(lcd_object, message, line, log):
    """
    Prints messages in display and stdout
    """
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    if log:
        print(f'{message} -  {date_time_str}')
    # if BINITLCD:
    lcd_object.lcd_string(message, line)


def logmessage(level, message):
    """
    logs messages to file
    """
    log_message = {'time_stamp': datetime.now(),
                   'level': level, 
                   'message': message}
    if level == 'info':
        logger.info(log_message)
    elif level ==  'error':
        logger.error(log_message)


def initInputDevice(queue):
    """
    """
    idev = detectInputDevice()
    if idev is not None:
        dev = connectInputDevice(idev)
        threading.Thread(target = readBarCodes, args = (dev, queue, pauseDevice, ), daemon = True).start()
        BJET = True
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
        printMessageDict(lcd, {LCDI2C.LCD_LINE_1: "LAN DETECTED", LCDI2C.LCD_LINE_2: ip})
        logmessage('info', f'LAN DETECTED {ip}')
        time.sleep(2)
    else:
        printMessageDict(lcd, {LCDI2C.LCD_LINE_1, "LAN NOT DETECTED"})
        logmessage('info', f'LAN NOT DETECTED')

    gm65q = queue.Queue(maxsize = 1)
    jet111q = queue.Queue(maxsize = 1)
    initGPIO()
    idev = initInputDevice(jet111q)
    if idev is not None:
        printMessageDict(lcd, {LCDI2C.LCD_LINE_2: "INPUT DEV ON"})
        logmessage('info', "INPUT DEV ON")
    else:
        printMessageDict(lcd, {LCDI2C.LCD_LINE_2: "INPUT DEV OFF"})
        logmessage('error', "INPUT DEV OFF")
        
    time.sleep(1)
    
    if "raspi" in platform.node() or "vehiculo" in platform.node():
        sp = None
    else:
        sp = initSerialDevice(gm65q)
        # if sp is not None:
        #     printMessage(lcd, "GM65 ON", LCDI2C.LCD_LINE_2, True)
        # else:
        #     printMessage(lcd, "GM65 OFF", LCDI2C.LCD_LINE_2, True)
        time.sleep(2)

    code = None
    while True:
        gm65data = None
        jet111data = None
        marked = False
        brestart = 1
        if "tango" in platform.node() or 'vehiculos' in platform.node():
            brestart = wiringpi.digitalRead(GPIO_RESTART)
        else:
            brestart = rasp_button_restart.pin.state

        if brestart == 0:
            printMessageDict(lcd, {LCDI2C.LCD_LINE_1: "REINICIANDO", LCDI2C.LCD_LINE_2: "YA VOLVEMOS..."})
            logmessage('info', 'RESTART REQUESTED')
            if fhandler is not None:
                fhandler.close()
            exit()

        if code is None:
            FAILURE_COUNT = 5
            if sp is not None:
                if not gm65q.empty():
                    gm65data = gm65q.get()
                    if gm65data is not None:     
                        printMessageDict(lcd, {LCDI2C.LCD_LINE_1: gm65data})
                        logmessage('info', f'{gm65data}')
                        code = gm65data
            if idev is not None:
                if not jet111q.empty():
                    jet111data = jet111q.get()
                    if jet111data is not None:
                        printMessageDict(lcd, {LCDI2C.LCD_LINE_1: jet111data})
                        logmessage('info', f'{jet111data}')
                        code = jet111data
                            
        bfinalize_job = False
        if (code is not None):
            pauseDevice.pauseDevice()
            result = apicall(code)
            logmessage('info', dumps(result))
            if result['apistatus'] == True:
                if result['code'] == False:
                    logmessage('error', f"{code} {result['m1']} {result['m2']}")
                    printMessageDict(lcd, {LCDI2C.LCD_LINE_1: result['m1'], LCDI2C.LCD_LINE_2: result['m2']})
                    time.sleep(1)
                else:
                    logmessage('info', f"{code} {result['m1']} {result['m2']}")
                    printMessageDict(lcd, {LCDI2C.LCD_LINE_1: result['m1'], LCDI2C.LCD_LINE_2: result['m2']})
                    marked = enableGate()
                    if marked:
                        logmessage('info', f'{code} marked')
                ticket_string = f'code: {code}, status:{result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
                bfinalize_job = True
            else:
                logmessage('error', f'FALLA DE SISTEMA - REINTENTANDO')
                printMessageDict(lcd, {LCDI2C.LCD_LINE_1: 'FALLA DE SISTEMA', LCDI2C.LCD_LINE_2: "REINTENTANDO"})
                FAILURE_COUNT -= 1
                ticket_string = f'code: {code}, status: api failed, timestamp: {datetime.now()} \n'
                if FAILURE_COUNT == 0:
                    logmessage('error', f'FALLA PERMANENTE - INFORME PROBLEMA')
                    printMessageDict(lcd, {LCDI2C.LCD_LINE_1: 'FALLA PERMANENTE', LCDI2C.LCD_LINE_2: "INFORME PROBLEMA"})
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
            printMessage(lcd, "CARNAVAL 2025", LCDI2C.LCD_LINE_1, False)
            printMessage(lcd, "NUEVO INGRESO", LCDI2C.LCD_LINE_2, False)


if __name__ == '__main__':
    main()