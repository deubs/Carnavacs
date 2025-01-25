#!/usr/bin/python
#--------------------------------------
#  molinete_system_v1.py 
#  Author: Emiliano Melchiori
#  Date: 28/11/2024
#  OrangePI Zero3 access control system
#  based on GM65 bar code scanner, NexuPOS Jet 111 bar code scanner, 16x2 LCD i2c, API calls 

import serial
import LCDI2Cv2
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

from gpiozero import Button, DigitalInputDevice, OutputDevice

print("importing gpiozero")
rasp_button_restart = Button(4, pull_up=True) # PIN 7
relay_outa = OutputDevice(17) # PIN 11
relay_outb = OutputDevice(16) # PIN 11
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


class baseAccessSystem(object):
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
        self.main()


    def connectInputDevice(self, inputdev):
        try:           
            device = InputDevice(inputdev) # Replace with your device
        except Exception as e:
            print(e)
            return None
        else:
            print(device)
            print(device.capabilities())
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


    def printMessage(self, message, line, log):
        """
        Prints messages in display and stdout
        """
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        if log:
            print(f'{message} -  {date_time_str}')
        # if BINITLCD:
        self.lcd.lcd_string(message, line)


    def initLCD(self):
        try:
            self.lcd = LCDI2Cv2.LCD()
            self.lcd.lcd_init(self.display_address)
            self.printMessage("LCD INIT", LCDI2Cv2.LCD_LINE_1, True)
            self.printMessage(platform.node(), LCDI2Cv2.LCD_LINE_2, True)
            time.sleep(2)
        except Exception as e:
            print(e)


    def detectLAN(self):
        BLAN, ip = checklan.checkLAN(checklan.target, checklan.timeout)
        if BLAN:
            self.printMessage("LAN DETECTED", LCDI2Cv2.LCD_LINE_1, True)
            self.printMessage(ip, LCDI2Cv2.LCD_LINE_2, True)
            time.sleep(2)
        else:
            self.printMessage("LAN NOT DETECTED", LCDI2Cv2.LCD_LINE_1, True)


    def enableGate(self):
        self.gpio_out.on()
        time.sleep(2)
        self.gpio_out.off()


    def initInputDevice(self, queue, inputdev):
        """
        """
        # idev = detectInputDevice()
        if inputdev is not None:
            dev = self.connectInputDevice(inputdev)
            threading.Thread(target = self.readBarCodes, args = (dev, queue, pauseDevice, ), daemon = True).start()
            BJET = True
        return idev


    def main(self):
        """
            Main function
        """
        self.initLCD()
        fhandler = self.createFile(workingdir=join('/home/pi', sysname=self.name))
        # gm65q = queue.Queue(maxsize = 1)
        jet111q = queue.Queue(maxsize = 1)
        idev = self.initInputDevice(jet111q, self.inputsystem)

        if idev is not None:
            self.printMessage("INPUT DEV ON", LCDI2Cv2.LCD_LINE_2, True)
        else:
            self.printMessage("INPUT DEV OFF", LCDI2Cv2.LCD_LINE_2, True)
        time.sleep(1)
        
        code = None
        while True:
            jet111data = None
            marked = False
            brestart = 1
            brestart = rasp_button_restart.pin.state

            if brestart == 0:
                self.printMessage("REINICIANDO", LCDI2Cv2.LCD_LINE_1, True)
                self.printMessage("YA VOLVEMOS...", LCDI2Cv2.LCD_LINE_2, True)
                if fhandler is not None:
                    fhandler.close()
                exit()

            if code is None:
                FAILURE_COUNT = 5
                if idev is not None:
                    if not jet111q.empty():
                        print("reading queue...jet111")
                        jet111data = jet111q.get()
                        if jet111data is not None:
                            self.printMessage(jet111data, LCDI2Cv2.LCD_LINE_1, True)
                            code = jet111data
                                
            bfinalize_job = False
            if (code is not None):
                pauseDevice.pauseDevice()
                result = self.apicall(code)
                if result['apistatus'] == True:
                    if result['code'] == False:
                        self.printMessage(result['m1'], LCDI2Cv2.LCD_LINE_1, True)
                        self.printMessage(result['m2'], LCDI2Cv2.LCD_LINE_2, True)
                        time.sleep(1)
                    else:
                        self.printMessage(result['m1'], LCDI2Cv2.LCD_LINE_1, True)
                        self.printMessage(result['m2'], LCDI2Cv2.LCD_LINE_2, True)
                        marked = self.enableGate()
                        if marked:
                            self.printMessage("CODIGO MARCADO", LCDI2Cv2.LCD_LINE_1, True)
                            self.printMessage("BIENVENIDO", LCDI2Cv2.LCD_LINE_2, True)
                    ticket_string = f'code: {code}, status:{result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
                    bfinalize_job = True
                else:
                    self.printMessage('FALLA DE SISTEMA', LCDI2Cv2.LCD_LINE_1, True)
                    self.printMessage("REINTENTANDO", LCDI2Cv2.LCD_LINE_2, True)
                    FAILURE_COUNT -= 1
                    ticket_string = f'code: {code}, status: api failed, timestamp: {datetime.now()} \n'
                    if FAILURE_COUNT == 0:
                        self.printMessage(lcd, "FALLA PERMANENTE", self.LCDI2Cv2.LCD_LINE_1, True)
                        self.printMessage(lcd, "INFORME PROBLEMA", self.LCDI2Cv2.LCD_LINE_2, True)
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
                self.printMessage("CARNAVAL 2025", LCDI2Cv2.LCD_LINE_1, False)
                self.printMessage("NUEVO INGRESO", LCDI2Cv2.LCD_LINE_2, False)

if __name__ == '__main__':

    inputa = '/dev/input/input21'
    inputb = '/dev/input/input22'
    
    asys = {"Proveedores1":{"gpio_out": relay_outa, "display_i2caddress": 0x27, "input_device": inputa}, 
            "Proveedores2":{"gpio_out": relay_outb, "display_i2caddress": 0x3F, "input_device": inputb}}
    
    asA = AccessSystem(name = "Proveedores1",
                       i2cdisplayaddress = asys['Proveedores1']["display_i2caddress"],
                       inputsystem = asys['Proveedores1']["input_device"], 
                       gpioout = asys['Proveedores1']['gpio_out'])
    
    asB = AccessSystem(name = "Proveedores2",
                       i2cdisplayaddress = asys['Proveedores2']["display_i2caddress"],
                       inputsystem = asys['Proveedores2']["input_device"], 
                       gpioout = asys['Proveedores2']['gpio_out'])