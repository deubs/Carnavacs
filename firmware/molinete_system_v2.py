#!/usr/bin/python
#--------------------------------------
#  molinete_system_v2.py 
#  Author: Emiliano Melchiori
#  Date: 28/01/2025
#  Raspberry Pi access control system
#  based on dual NexuPOS Jet 111 bar code scanner, 16x2 LCD i2c, API calls 

import os
import LCDI2Cv2
import threading
import queue
import time
# import checklan
from requests import post, get, exceptions, Session
from datetime import datetime, date
import socket
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
import structlog

# Optional: psutil for system metrics (graceful fallback if not available)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

print("importing gpiozero")
rasp_button_restart = Button(4, pull_up=True) # PIN 7
relay_outa = OutputDevice(17) # PIN 11
relay_outb = OutputDevice(27) # PIN 11
workingdir = "/home/pi"
print(workingdir)

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
BJET = False
# ORANGE PI ZERO 3 WIRING

apiurlb = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurl = "http://192.168.40.100/Ticket/Validate"

# Dashboard server URL for health reporting and remote commands
DASHBOARD_URL = os.environ.get('DASHBOARD_URL', 'http://192.168.40.251:5000')
DEVICE_NAME = platform.node()
HEALTH_REPORT_INTERVAL = 30  # seconds
COMMAND_POLL_INTERVAL = 10   # seconds

# threading_event = threading.Event()
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'_', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
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

logger.info(
        "device_status",
        workingdir=workingdir,
        scancodes=scancodes,
        network_status="online",
)

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
        log = getattr(logger, level)
        log(message)


    def enableGate(self):
        self.gpio_out.on()
        time.sleep(1.5)
        self.gpio_out.off()
        return True


    def initInputDevice(self, queue):
        """
        """
        if self.inputsystem is not None:
            dev = self.connectInputDevice()
            threading.Thread(target = self.readBarCodes, args = (dev, queue, pauseDevice, ), daemon = True).start()
            self.logmessage('info', 'input device connected')
            BJET = True
        return dev


    def checkCode(self, code:str):
        """
            Reboot and Shutdown codes
        """
        if code == '00000000000100000000000':
            self.logmessage('info', 'REBOOT REQUIRED BY QR')
            self.lcd.lcd_string("REBOOT BY QR", l1, self.display_address)
            self.lcd.lcd_string("REBOOT BY QR", l2, self.display_address)
            os.system('reboot')
            time.sleep(5)
        if code == "11111111111111111111111":
            self.logmessage('info', 'SHUT DOWN REQUIRED BY QR')
            self.lcd.lcd_string("SHUTDOWN BY QR", l1, self.display_address)
            self.lcd.lcd_string("SHUTDOWN BY QR", l2, self.display_address)
            os.system('systemctl poweroff')
            time.sleep(5)
        if code == "22222222222222222222222":
            self.logmessage('info', 'LCD RESTART BY QR')
            self.lcd.lcd_string("LCD RESTART BY QR", l1, self.display_address)
            self.lcd.lcd_string("LCD RESTART BY QR", l2, self.display_address)
            self.lcd.initDisplay(self.display_address)
            

    def main(self, lcd):
        """
            Main function
        """
        ncodes = 0
        bdirt = False
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
        bdirt = True
        nloops = 0
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
            nloops += 1
            if code is None:
                FAILURE_COUNT = 5
                if idev is not None:
                    if not jet111q.empty():
                        # print("reading queue...jet111")
                        jet111data = jet111q.get()
                        if jet111data is not None:
                            self.lcd.lcd_string(f'{jet111data}', l1, self.display_address)
                            code = jet111data
                            # time.sleep(0.5)
                else:
                    self.lcd.lcd_string("PISTOLA", l1, self.display_address)
                    self.lcd.lcd_string("DESCONECTADA", l1, self.display_address)

            bfinalize_job = False
            if (code is not None):
                ncodes += 1
                pauseDevice.pauseDevice()
                self.checkCode(code)
                result = self.apicall(code)
                # result = {'apistatus': True, 'code': code, 'm1': 'holis', 'm2': 'troesma'}
                self.logmessage('info', f'{code} - {dumps(result)}')
                if result['apistatus'] == True:
                    self.lcd.lcd_string(f'{result["m1"]}', l1, self.display_address)
                    self.lcd.lcd_string(f'{result["m2"]}', l2, self.display_address)
                    if result['code'] == False:
                        time.sleep(1)
                    else:
                        marked = self.enableGate()
                        if marked:
                            self.logmessage('info', 'CODIGO MARCADO {code}')
                            # self.lcd.lcd_string(f'CODIGO MARCADO', l1, self.display_address)
                            # self.lcd.lcd_string(f'BIENVENIDO', l2, self.display_address)
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
                    bdirt = True
                    code = None
                    pauseDevice.resumeDevice()
                    if ncodes > 5:
                        self.lcd.initDisplay(self.display_address)
                        ncodes = 0 
                if fhandler is not None:
                    fhandler.write(ticket_string)
                    fhandler.flush()
            else:
                # if bdirt:
                self.lcd.lcd_string("CARNAVAL 2026", l1, self.display_address)
                self.lcd.lcd_string("NUEVO INGRESO", l2, self.display_address)
                if nloops > 20:
                    self.lcd.initDisplay(self.display_address)
                    nloops = 0
                    ncodes = 0
                    # self.lcd.lcd_string("LCD init", l2, self.display_address)
                
                # bdirt = False
                # code = None

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

# ============================================
# Health Reporting & Remote Command System
# ============================================

def get_local_ip():
    """Get the local IP address of the device"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"

def check_server_reachable():
    """Check if dashboard server is reachable"""
    try:
        get(f"{DASHBOARD_URL}/", timeout=2)
        return True
    except:
        return False

def check_i2c_display(address):
    """Check if I2C display is responding"""
    try:
        bus.read_byte(address)
        return True
    except:
        return False

def get_system_temperature():
    """Get CPU temperature (Raspberry Pi / Orange Pi)"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
            return round(temp, 1)
    except:
        return None

def get_device_health(scanner_threads_active=True, display_addresses=None):
    """Collect device health metrics"""
    health = {
        "device": DEVICE_NAME,
        "ip": get_local_ip(),
        "timestamp": datetime.now().isoformat(),
        "network": {
            "connected": True,  # If we're reporting, network is up
            "server_reachable": check_server_reachable(),
            "ip_address": get_local_ip()
        },
        "scanner": {
            "connected": scanner_threads_active,
            "device_name": "IMAGER 2D"
        },
        "display": {
            "connected": False,
            "i2c_addresses": []
        },
        "system": {}
    }

    # Check displays
    if display_addresses:
        connected_displays = []
        for addr in display_addresses:
            if check_i2c_display(addr):
                connected_displays.append(hex(addr))
        health["display"]["connected"] = len(connected_displays) > 0
        health["display"]["i2c_addresses"] = connected_displays

    # System metrics (if psutil available)
    if PSUTIL_AVAILABLE:
        health["system"]["cpu_percent"] = psutil.cpu_percent(interval=0.1)
        health["system"]["memory_percent"] = psutil.virtual_memory().percent
        health["system"]["disk_percent"] = psutil.disk_usage('/').percent

    # Temperature
    temp = get_system_temperature()
    if temp:
        health["system"]["temperature"] = temp

    # Uptime
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.read().split()[0])
            health["uptime_seconds"] = int(uptime_seconds)
    except:
        pass

    return health

def health_reporter_thread(interval=HEALTH_REPORT_INTERVAL, scanner_threads_ref=None, display_addresses=None):
    """Background thread that reports health every N seconds"""
    logger.info("health_reporter_started", interval=interval)
    while True:
        try:
            # Check if scanner threads are still active
            scanner_active = True
            if scanner_threads_ref:
                current_threads = [t.name for t in threading.enumerate()]
                scanner_active = any('readBarCodes' in name or 'Thread' in name for name in current_threads)

            health = get_device_health(
                scanner_threads_active=scanner_active,
                display_addresses=display_addresses
            )
            post(f"{DASHBOARD_URL}/api/health", json=health, timeout=5)
            logger.info("health_reported", device=DEVICE_NAME, cpu=health["system"].get("cpu_percent"))
        except Exception as e:
            logger.warning("health_report_failed", error=str(e))
        time.sleep(interval)

def execute_remote_command(command, lcd=None, display_address=None):
    """Execute a remote command received from dashboard"""
    logger.info("remote_command_received", command=command)

    if lcd and display_address:
        lcd.lcd_string(f"CMD: {command.upper()}", l1, display_address)

    if command == 'reboot':
        if lcd and display_address:
            lcd.lcd_string("REBOOTING...", l2, display_address)
        logger.info("remote_command_executing", command="reboot")
        time.sleep(2)
        os.system('reboot')
    elif command == 'shutdown':
        if lcd and display_address:
            lcd.lcd_string("SHUTTING DOWN", l2, display_address)
        logger.info("remote_command_executing", command="shutdown")
        time.sleep(2)
        os.system('systemctl poweroff')
    elif command == 'restart_service':
        if lcd and display_address:
            lcd.lcd_string("RESTARTING SVC", l2, display_address)
        logger.info("remote_command_executing", command="restart_service")
        time.sleep(2)
        os.system('systemctl restart molinete')
    elif command == 'lcd_init':
        if lcd and display_address:
            lcd.initDisplay(display_address)
            lcd.lcd_string("LCD REINIT", l2, display_address)
        logger.info("remote_command_executing", command="lcd_init")
    else:
        logger.warning("unknown_remote_command", command=command)

def command_poller_thread(interval=COMMAND_POLL_INTERVAL, lcd=None, display_address=None):
    """Background thread that polls for remote commands"""
    logger.info("command_poller_started", interval=interval)
    while True:
        try:
            resp = get(f"{DASHBOARD_URL}/api/commands/{DEVICE_NAME}", timeout=5)
            data = resp.json()
            cmd = data.get('command')
            if cmd:
                execute_remote_command(cmd, lcd=lcd, display_address=display_address)
        except Exception as e:
            # Silent fail - server might be unreachable
            pass
        time.sleep(interval)


if __name__ == '__main__':

    display_addressa = 0x26
    display_addressb = 0x27

    lcd = LCDI2Cv2.LCD()
    lcd.lcd_init(display_addressa, display_addressb)
    
    lcd.lcd_string("LCD INIT", l1, display_addressa)
    lcd.lcd_string(platform.node(), l2, display_addressa)
    
    lcd.lcd_string("LCD INIT", l1, display_addressb)
    lcd.lcd_string(platform.node(), l2, display_addressb)

    # Start health reporter thread
    display_addresses_list = [display_addressa, display_addressb]
    threading.Thread(
        target=health_reporter_thread,
        args=(HEALTH_REPORT_INTERVAL, None, display_addresses_list),
        daemon=True,
        name="HealthReporter"
    ).start()

    # Start command poller thread (uses display_addressa for messages)
    threading.Thread(
        target=command_poller_thread,
        args=(COMMAND_POLL_INTERVAL, lcd, display_addressa),
        daemon=True,
        name="CommandPoller"
    ).start()

    logger.info("monitoring_threads_started", health_interval=HEALTH_REPORT_INTERVAL, command_interval=COMMAND_POLL_INTERVAL)

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

    # nthreads = threading.enumerate()
    while True:
        time.sleep(10)
        continue
    

    lcd.lcd_string("EXIT", l1, display_addressa)
    lcd.lcd_string(platform.node(), l2, display_addressa)
    
    lcd.lcd_string("EXIT", l1, display_addressb)
    lcd.lcd_string(platform.node(), l2, display_addressb)

    exit()