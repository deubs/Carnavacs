#!/usr/bin/python
#--------------------------------------
#  molinete_system_v1.py 
#  Author: Emiliano Melchiori
#  Date: 28/11/2024
#  OrangePI Zero3 access control system
#  based on GM65 bar code scanner, NexuPOS Jet 111 bar code scanner, 16x2 LCD i2c, API calls 

import serial
import LCDI2C
from JET111_Thread import detectDevice, connectDevice, readBarCodes
import threading
import queue
import time
import wiringpi
import checklan
from requests import post
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

apiurl = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurlb = "https://api.carnavaldelpais.com.ar/Ticket/Validate"

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
    # wiringpi.digitalWrite(GPIO_RELAY_OUT1, wiringpi.GPIO.HIGH)
    wiringpi.digitalWrite(GPIO_RELAY_OUT2, wiringpi.GPIO.HIGH)
    bHole = ISRSignal()
    if not bHole:
        print("Activate RELAYS")
        # wiringpi.digitalWrite(GPIO_RELAY_OUT1, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(GPIO_RELAY_OUT2, wiringpi.GPIO.LOW)
        return True
    return False


def printSTATUS():
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
    apimessage = response['message']
    ticketstatus = response['result']['ticketStatus']
    name = response['result']['ticketStatus']['name']
    ticketId = response['result']['ticketId']
    isValid = response['result']['isValid']
    ticketExists = response['result']['exists']
    return {'code': isValid and ticketExists,'text': name}


def apicall(code):
    apikey = keys['key1']
    header = {
        'X-API-Key': f'{apikey}',
        'Content-Type': "application/json"
    }
    payload = {'code': code}
    try:
        response = post(apiurlb, params=payload, headers=header)
        if response.status_code == 200:
            result = processResponse(response.json())
            return result
        if response.status_code == 401:
            print(response.content)
            return {'code':401, 'status':401}
    except Exception as e:
        print(e)
        return {'': ''}
     
lcd = initLCD()

def createFile():
    dt = datetime.now().isoformat()
    fname = f'tickets_{dt}.txt'
    f = open(fname, "a")
    return f

def main():
    """
        Main function
    """
    fhandler =  createFile()

    BLAN = checklan.checkLAN(checklan.target, checklan.timeout)
    if BLAN:
        lcd.lcd_string("LAN is OK", LCDI2C.LCD_LINE_1)
    else:
        lcd.lcd_string("LAN is OFF", LCDI2C.LCD_LINE_1)

    gm65q = queue.Queue()
    jet111q = queue.Queue()    
    initGPIO()
    sp = initSerialPort()
    idev = detectDevice()
    if idev is not None:
        dev = connectDevice(idev)
        threading.Thread(target = readBarCodes, args = (dev, jet111q,), daemon = True).start()
        lcd.lcd_string("JET111 OK...", LCDI2C.LCD_LINE_1)
        BJET = True

    if sp != None:
        lcd.lcd_string('GM65 OK...', LCDI2C.LCD_LINE_2)
        threading.Thread(target = readPort, args = (sp, gm65q,), daemon = True).start()
        BGM65 = True
        code = None
        time.sleep(2)
        while True:
            gm65data = None
            jet111data = None
            marked = False
            if code is None:
                if not gm65q.empty():
                    print("reading queue...gm65")
                    gm65data = gm65q.get()
                    if gm65data is not None:     
                        print("Barcode: " + gm65data)
                        lcd.lcd_string(gm65data, LCDI2C.LCD_LINE_1)
                        code = gm65data            
            if code is None:
                if not jet111q.empty():
                    print("reading queue...jet111")
                    jet111data = jet111q.get()
                    if jet111data is not None:           
                        print("Barcode: " + jet111data)
                        lcd.lcd_string(jet111data, LCDI2C.LCD_LINE_1)
                        code = jet111data
            if code is not None:
                print(code)
                result = apicall(code)
                if result['code'] == False:
                    # print("INVALID CODE")
                    lcd.lcd_string(code, LCDI2C.LCD_LINE_1)
                    lcd.lcd_string(result['text'], LCDI2C.LCD_LINE_2)
                else:
                    lcd.lcd_string(code, LCDI2C.LCD_LINE_1)
                    lcd.lcd_string("BIENVENIDO", LCDI2C.LCD_LINE_2)
                    marked = enableGate()
                    if marked:
                        print("MARKED CODE")
                        ticket_string = f'code: {code}, status:{code}, timestamp: {datetime.now()} \n'
                        fhandler.write(ticket_string)
                        fhandler.flush()
                        code = None
                    
    else:
        lcd.lcd_string("Serial Port Fail", LCDI2C.LCD_LINE_1)
        lcd.lcd_string("Input Fail", LCDI2C.LCD_LINE_2)

if __name__ == '__main__':
    main()