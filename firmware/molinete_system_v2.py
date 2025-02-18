#!/usr/bin/python
#--------------------------------------
#  molinete_system_v2.py 
#  Author: Emiliano Melchiori
#  Date: 28/01/2025
#  Raspberry Pi access control system
#  based on dual NexuPOS Jet 111 bar code scanner, 16x2 LCD i2c, API calls 

import LCDI2Cv2
import threading
import queue
import time
import checklan
from requests import post, exceptions, Session
from datetime import datetime, date
from apikeys import keys
from evdev import InputDevice, categorize, ecodes, list_devices
import platform
from os import makedirs
from os.path import exists, join
from gpiozero import Button, DigitalInputDevice, OutputDevice
import logging
import logging.handlers
from json import dumps
import smbus2 as smbus


print("importing gpiozero")
rasp_button_restart = Button(4, pull_up=True) # PIN 7
relay_outa = OutputDevice(17) # PIN 11
relay_outb = OutputDevice(27) # PIN 11
workingdir = "/home/pi"
print(workingdir)

logging.basicConfig(filename= f"{workingdir}/logs/{platform.node()}_{date.today().isoformat()}.log",
                    filemode='a',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger()


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

l1 = LCDI2Cv2.LCD_LINE_1
l2 = LCDI2Cv2.LCD_LINE_2

class PauseDeviceTOKEN:
    def __init__(self):
        self.is_paused = False
    
    def pauseDevice(self):
        self.is_paused = True
    
    def resumeDevice(self):
        self.is_paused = False

pauseDevice = PauseDeviceTOKEN()

bus = smbus.SMBus(1)  # Rev 1 Pi uses 0
    
class baseAccessSystem():
    def __init__(self):
        pass


    def createFile(self, workingdir, sysname):
        """
            Creates log file for read codes, returns file handler
        """
        fdir = join(workingdir, 'tickets')
        if not exists(fdir):
            makedirs(fdir)
        f = None
        dt = date.today().isoformat()
        try:
            fname = join(fdir, f'tickets_{sysname}_{dt}.txt')
            f = open(fname, "a")
        except Exception as e:
            print(e)
        return f


    def processResponse(self, response):
        apistatus = response['success']
        isValid = response['result']['isValid']
        m1 = response['result']['m1']
        m2 = response['result']['m2']
        return {'apistatus': apistatus, 'code': isValid, 'm1': m1, 'm2': m2}


    def apicall(self, code):
        apikey = keys['key1']
        header = {
            'X-API-Key': f'{apikey}',
            'Content-Type': "application/json"
        }
        payload = {'code': code}
        try:
            response = post(apiurl, params=payload, headers=header, timeout=3)
            if response.status_code == 200:
                return self.processResponse(response.json())
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

class AccessSystem(baseAccessSystem):
    def __init__(self, 
                 i2cdisplayaddress, 
                 inputsystem,
                 gpioout,
                 name):

        self.display_address = i2cdisplayaddress
        self.inputsystem = inputsystem
        self.gpio_out = gpioout
        self.lcd = None
        self.name = name
        self.logger = logger
        self.bus = bus
        # self.main()


    def connectInputDevice(self):
        try:           
            device = InputDevice(self.inputsystem) # Replace with your device
        except Exception as e:
            self.logmessage('error', e)
            return None
        else:
            self.logmessage('info', device.name)
            return device


    def readBarCodes(self, device, q: queue, pause: PauseDeviceTOKEN):
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


    def logmessage(self, level, message):
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
        elif level ==  'critical':
            logger.critical(log_message)
        

    def enableGate(self):
        self.gpio_out.on()
        time.sleep(2)
        self.gpio_out.off()


    def initInputDevice(self, queue):
        """
        """
        if self.inputsystem is not None:
            dev = self.connectInputDevice()
            threading.Thread(target = self.readBarCodes, args = (dev, queue, pauseDevice, ), daemon = True).start()
            self.logmessage('info', 'input device connected')
            BJET = True
        return dev


    def main(self, lcd):
        """
            Main function
        """
        # self.initLCD()
        self.lcd = lcd
        print(self.lcd)
        print(self.display_address)
        fhandler = self.createFile(workingdir = workingdir, sysname = self.name)
        jet111q = queue.Queue(maxsize = 1)
        idev = self.initInputDevice(jet111q)
        if idev is not None:
            self.lcd.lcd_string("INPUT DEV ON", l2, self.display_address)
            self.logmessage('info', "INPUT DEV ON")
        else:
            self.lcd.lcd_string("INPUT DEV OFF", l2, self.display_address)
            self.logmessage('error', "INPUT DEV OFF")

        time.sleep(1)
        nthreads =  threading.enumerate()
        code = None
        while True:
            jet111data = None
            marked = False
            brestart = 1
            brestart = rasp_button_restart.pin.state

            if nthreads != threading.enumerate():
                brestart = 0
                self.logmessage('critical', 'INPUT DEVICE IS DISCONNECTED. INFORM')
                self.lcd.lcd_string("PISTOLA", l1, self.display_address)
                self.lcd.lcd_string("DESCONECTADA", l1, self.display_address)

            if brestart == 0:
                self.lcd.lcd_string("REINICIANDO", l1, self.display_address)
                self.lcd.lcd_string("YA VOlVEMOS", l2, self.display_address)
                if fhandler is not None:
                    fhandler.close()
                self.logmessage('error', 'RESTART REQUIRED')
                exit()

            if code is None:
                FAILURE_COUNT = 5
                if idev is not None:
                    if not jet111q.empty():
                        # print("reading queue...jet111")
                        jet111data = jet111q.get()
                        if jet111data is not None:
                            self.lcd.lcd_string(jet111data, l1, self.display_address)
                            code = jet111data
                else:
                    self.lcd.lcd_string("PISTOLA", l1, self.display_address)
                    self.lcd.lcd_string("DESCONECTADA", l1, self.display_address)

            bfinalize_job = False
            if (code is not None):
                # pauseDevice.pauseDevice()
                result = self.apicall(code)
                self.logmessage('info', f'{code} - {dumps(result)}')
                if result['apistatus'] == True:
                    self.lcd.lcd_string(result['m1'], l1, self.display_address)
                    self.lcd.lcd_string(result['m2'], l2, self.display_address)
                    if result['code'] == False:
                        time.sleep(1)
                    else:
                        marked = self.enableGate()
                        if marked:
                            self.lcd.lcd_string('CODIGO MARCADO', l1, self.display_address)
                            self.lcd.lcd_string('BIENVENIDO', l2, self.display_address)
                    ticket_string = f'code: {code}, status:{result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
                    bfinalize_job = True
                else:
                    self.lcd.lcd_string("FALLA DE SISTEMA", l1, self.display_address)
                    self.lcd.lcd_string("REINTENTANDO", l2, self.display_address)
                    FAILURE_COUNT -= 1
                    ticket_string = f'code: {code}, status: api failed, timestamp: {datetime.now()} \n'
                    if FAILURE_COUNT == 0:
                        self.lcd.lcd_string("FALLA PERMANENTE", l1, self.display_address)
                        self.lcd.lcd_string("INFORME PROBLEMA", l2, self.display_address)
                        time.sleep(2)
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
                self.lcd.lcd_string("CARNAVAL 2015", l1, self.display_address)
                self.lcd.lcd_string("NUEVO INGRESO", l2, self.display_address)

def getInputDevices():
    devices = [InputDevice(path) for path in list_devices()]
    inputdevs = []
    for device in devices:
        print(device.name)
        if ("IMAGER 2D" in device.name) or \
            ("BF SCAN SCAN KEYBOARD" in device.name) or \
                ("NT USB Keyboard" in device.name) or \
                    ("ZKRFID R400" in device.name) or \
                        ("TMS HIDKeyBoard" in device.name) or \
                            ("BARCODE SCANNER Keyboard Interface" in device.name):
            inputdevs.append(device)
    return inputdevs

import pdb

from multiprocessing import Process

if __name__ == '__main__':

    display_addressa = 0x26
    display_addressb = 0x27

    lcd = LCDI2Cv2.LCD()
    lcd.lcd_init(display_addressa, display_addressb)
    
    lcd.lcd_string("LCD INIT", l1, display_addressa)
    lcd.lcd_string(platform.node(), l2, display_addressa)
    
    lcd.lcd_string("LCD INIT", l1, display_addressb)
    lcd.lcd_string(platform.node(), l2, display_addressb)

    idevs = getInputDevices() 
    if len(idevs) > 1:
        asys = {"Proveedores1":{"gpio_out": relay_outa, "display_i2caddress": 0x27, "input_device": idevs[0]}, 
                "Proveedores2":{"gpio_out": relay_outb, "display_i2caddress": 0x26, "input_device": idevs[1]}}


    asA = AccessSystem(name = "Proveedores1",
                    i2cdisplayaddress = asys['Proveedores1']["display_i2caddress"],
                    inputsystem = asys['Proveedores1']["input_device"], 
                    gpioout = asys['Proveedores1']['gpio_out'])
    
    threading.Thread(target = asA.main, args = (lcd, ), daemon = True).start()
    # pa = Process(target= asA.main, args=(lcd, ))
    # pa.start()
    asB = AccessSystem(name = "Proveedores2",
                        i2cdisplayaddress = asys['Proveedores2']["display_i2caddress"],
                        inputsystem = asys['Proveedores2']["input_device"], 
                        gpioout = asys['Proveedores2']['gpio_out'])
    # pb = Process(target= asB.main, args=(lcd, ))
    threading.Thread(target = asB.main, args = (lcd, ), daemon = True).start()
    # pb.start()

    while True:
        time.sleep(10)
        continue