#!/usr/bin/python
#--------------------------------------
#  molinete_system_v1.py 
#  Author: Emiliano Melchiori
#  Date: 28/11/2024
#  OrangePI Zero3 access control system
#  based on GM65 bar code scanner, NexuPOS Jet 111 bar code scanner, 16x2 LCD i2c, API calls 

import serial
import LCDI2C
import JET111_Thread
from JET111_Thread import detectDevice, connectDevice, readBarCodes
import threading
import queue
import time
import wiringpi
import checklan
from requests import post, exceptions, Session
from datetime import datetime
from apikeys import keys


# STATUS VARS
BLAN = False
BGM65 = False
BJET = False
# ORANGE PI ZERO 3 WIRING
I2CBUS = 3
# GPIO_RELAY_OUT1 = 9 #PC15
GPIO_RELAY_OUT2 = 10 #PC14
GPIO_INPUT_1 = 13   #PC7

apiurlb = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurl = "http://192.168.40.100/Ticket/Validate"

# BCODEREAD_ENABLED = True
def readPort(serialP, q:queue):
    """
        Serial port communication with GM65 barcode reader
    """
    print("Serial Port Opened")
    breading = True
    if serialP.isOpen():
        while breading:
            print("Reading Serial Port")
            data = ""
            while True:
                if JET111_Thread.BINPUT_CODE_READ_ENABLED:
                    if q.empty():
                        cmdRet = serialP.read().decode()
                        if (cmdRet == '\r' or cmdRet == '\n'):
                            q.put(data)
                            break
                        else:
                            data += str(cmdRet)
            # print("Raw1 = " + str(data))
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


def initLCD():
    """
        Initiates LCD
    """
    lcd = LCDI2C.LCD()
    lcd.lcd_init()
    return lcd

bGATEOPEN = False

def ISRSignal():
    """
        
    """
    print("Reading inductive...")
    bGATEOPEN = False
    bwait4Hole = True
    print("State is HIGH...")
    while bwait4Hole:
        state = None
        bwait4Hole = wiringpi.digitalRead(GPIO_INPUT_1)
    print("State is LOW")
    return bwait4Hole


def initGPIO():
    """
        Initiates GPIO.
        OPIz3 using GPIO 17 and 18 for relays and 19 for inductive sensors.
    """
    print("INIT GPIO")
    wiringpi.wiringPiSetup()
    # wiringpi.pinMode(GPIO_RELAY_OUT1, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(GPIO_RELAY_OUT2, wiringpi.GPIO.OUTPUT)
    # wiringpi.digitalWrite(GPIO_RELAY_OUT1, wiringpi.GPIO.LOW)
    wiringpi.digitalWrite(GPIO_RELAY_OUT2, wiringpi.GPIO.LOW)
    wiringpi.pinMode(GPIO_INPUT_1, wiringpi.GPIO.INPUT)
    wiringpi.pullUpDnControl(GPIO_INPUT_1, wiringpi.GPIO.PUD_UP)
    # try:
    #     wiringpi.wiringPiISR(GPIO_INPUT_1, wiringpi.GPIO.INT_EDGE_FALLING, ISRSignal)
    # except Exception as e:
    #     print(e)


def wait_1sec():
    """
        WAIT 1 SEC
    """
    time.sleep(1)


def enableGate():
    """
    Dissable COIL using relays. Iluminate GREEN light 
    Wait until signal from inductive sensor
    Enable COIL releasing relays. Iluminate RED light
    """
    print("Realease RELAYS")
    wiringpi.digitalWrite(GPIO_RELAY_OUT2, wiringpi.GPIO.HIGH)
    bHole = ISRSignal()
    if not bHole:
        print("Activate RELAYS")
        wiringpi.digitalWrite(GPIO_RELAY_OUT2, wiringpi.GPIO.LOW)
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
        lcd = initLCD()
        BINITLCD = True
    except Exception as e:
        print(e)
        BINITLCD = False
    return lcd


bFILECREATED =  False
def createFile():
    f = None
    dt = datetime.now().isoformat()
    try:
        fname = f'tickets_{dt}.txt'
        f = open(fname, "a")
        bFILECREATED = True
    except Exception as e:
        print(e)
    return f

def printMessage(lcd_object, message, line):
    print(message)
    if BINITLCD:
        lcd_object.lcd_string(message, l)


def initInputDevice(queue):
    idev = detectDevice()
    if idev is not None:
        dev = connectDevice(idev)
        threading.Thread(target = readBarCodes, args = (dev, queue,), daemon = True).start()
        # printMessage(lcd, "JET111 OK...", LCDI2C.LCD_LINE_1)
        # lcd.lcd_string("JET111 OK...", LCDI2C.LCD_LINE_1)
        BJET = True
    return idev

def initSerialDevice(queue):
    sp = initSerialPort()
    if sp != None:
        # lcd.lcd_string('GM65 OK...', LCDI2C.LCD_LINE_2)
        # printMessage(lcd, 'GM65 OK...', LCDI2C.LCD_LINE_2)
        threading.Thread(target = readPort, args = (sp, queue,), daemon = True).start()
        BGM65 = True
        time.sleep(2)
    return sp



def main():
    """
        Main function
    """
    lcd = initLCD()
    print(lcd)
    fhandler = createFile()

    BLAN = checklan.checkLAN(checklan.target, checklan.timeout)
    if BLAN:
        printMessage(lcd, "LAN IS OK", LCDI2C.LCD_LINE_1)
    else:
        printMessage(lcd, "LAN IS OFF", LCDI2C.LCD_LINE_1)

    gm65q = queue.Queue(maxsize = 1)
    jet111q = queue.Queue(maxsize = 1)
    initGPIO()
    idev = initInputDevice(jet111q)
    sp = initSerialDevice(gm65q)

    code = None
    while True:
        gm65data = None
        jet111data = None
        marked = False
        if code is None:
            FAILURE_COUNT = 5
            if sp is not None:
                if not gm65q.empty():
                    JET111_Thread.BINPUT_CODE_READ_ENABLED = False
                    print("reading queue...gm65")
                    gm65data = gm65q.get()
                    if gm65data is not None:     
                        printMessage(lcd, gm65data, LCDI2C.LCD_LINE_1)
                        code = gm65data
            else:
                # serial device is OFF, try reconnect
                try:
                    sp = initSerialDevice(gm65q)
                except Exception as e:
                    printMessage(lcd, e, LCDI2C.LCD_LINE_1)

            if idev is not None:
                if not jet111q.empty():
                    JET111_Thread.BINPUT_CODE_READ_ENABLED = False
                    print("reading queue...jet111")
                    jet111data = jet111q.get()
                    if jet111data is not None:
                        printMessage(lcd, jet111data, LCDI2C.LCD_LINE_1)
                        code = jet111data
            else:
                # input device is OFF try reconnect
                printMessage(lcd, "INPUT DEVICE OFF", LCDI2C.LCD_LINE_1)
                try:
                    idev = initInputDevice(jet111q)
                except Exception as e:
                    printMessage(lcd, e, LCDI2C.LCD_LINE_1)

        if code is not None:
            result = apicall(code)
            print(result)
            if result['apistatus'] == True:
                if result['code'] == False:
                    printMessage(lcd, result['m1'], LCDI2C.LCD_LINE_1)
                    printMessage(lcd, result['m2'], LCDI2C.LCD_LINE_2)
                    time.sleep(3)
                else:
                    printMessage(lcd, result['m1'], LCDI2C.LCD_LINE_1)
                    printMessage(lcd, result['m2'], LCDI2C.LCD_LINE_2)
                    marked = enableGate()
                    if marked:
                        printMessage(lcd, "CODIGO MARCADO", LCDI2C.LCD_LINE_1)
                        printMessage(lcd, "BIENVENIDO", LCDI2C.LCD_LINE_2)
                        code = None
                        JET111_Thread.BINPUT_CODE_READ_ENABLED =  True
            else:
                # enableGate()
                lcd.lcd_string('FALLA DE SISTEMA', LCDI2C.LCD_LINE_1)
                lcd.lcd_string("REINTENTANDO", LCDI2C.LCD_LINE_2)
                # time.sleep(2)
                FAILURE_COUNT -= 1
                if FAILURE_COUNT == 0:
                    lcd.lcd_string("FALLA PERMANENTE", LCDI2C.LCD_LINE_1)
                    lcd.lcd_string("INFORME PROBLEMA", LCDI2C.LCD_LINE_2)
                    BINPUT_CODE_READ_ENABLED =  True
                    code = None

            ticket_string = f'code: {code}, status:{result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
            # ticket_string = f'code: {code}, timestamp: {datetime.now()} \n'
            if fhandler is not None:
                fhandler.write(ticket_string)
                fhandler.flush()
        else:
            printMessage(lcd, "CARNAVAL 2025", LCDI2C.LCD_LINE_1)
            printMessage(lcd, "NUEVO INGRESO", LCDI2C.LCD_LINE_1)

                    
    # else:
    #     lcd.lcd_string("Serial Port Fail", LCDI2C.LCD_LINE_1)
    #     lcd.lcd_string("Input Fail", LCDI2C.LCD_LINE_2)

if __name__ == '__main__':
    main()