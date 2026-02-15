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
DASHBOARD_URL = os.environ.get('DASHBOARD_URL', 'http://192.168.40.244')
DEVICE_NAME = platform.node()
HEALTH_REPORT_INTERVAL = 10  # seconds
COMMAND_POLL_INTERVAL = 5   # seconds

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

# Scanner watchdog settings
SCANNER_WATCHDOG_INTERVAL = 5  # Check scanner every 5 seconds
SCANNER_RECONNECT_DELAY = 3    # Wait 3 seconds between reconnect attempts

# Global registry of scanner managers for health reporting
scanner_managers = {}


class ScannerManager:
    """Manages USB scanner connection with auto-reconnect capability"""

    KNOWN_SCANNERS = [
        "IMAGER 2D", "BF SCAN SCAN KEYBOARD", "NT USB Keyboard",
        "TMS HIDKeyBoard", "ZKRFID R400", "BARCODE SCANNER"
    ]

    def __init__(self, name, code_queue, pause_token, lcd=None, display_address=None, initial_device=None):
        self.name = name
        self.code_queue = code_queue
        self.pause_token = pause_token
        self.lcd = lcd
        self.display_address = display_address
        self.device = None
        self.device_path = None
        self.device_name = None
        self.reader_thread = None
        self.connected = False
        self.running = True

        # Stats for health reporting
        self.disconnect_count = 0
        self.reconnect_count = 0
        self.last_disconnect_time = None
        self.last_reconnect_time = None

        self._lock = threading.Lock()

        # If initial device provided, use it
        if initial_device:
            self.device = initial_device
            self.device_path = initial_device.path
            self.device_name = initial_device.name
            self.connected = True

        # Register globally for health reporting
        scanner_managers[name] = self

    def detect_scanner(self, exclude_paths=None):
        """Detect available scanner device not in exclude list"""
        exclude_paths = exclude_paths or []
        try:
            devices = [InputDevice(path) for path in list_devices()]
            for device in devices:
                if device.path in exclude_paths:
                    continue
                if any(name in device.name for name in self.KNOWN_SCANNERS):
                    return device
        except Exception as e:
            logger.warning("scanner_detect_error", manager=self.name, error=str(e))
        return None

    def connect(self, device=None):
        """Connect to scanner device"""
        with self._lock:
            try:
                if device:
                    self.device = device
                else:
                    # Get paths of other connected scanners to avoid conflicts
                    exclude = [m.device_path for n, m in scanner_managers.items()
                              if n != self.name and m.device_path]
                    self.device = self.detect_scanner(exclude_paths=exclude)

                if self.device is None:
                    logger.warning("scanner_not_found", manager=self.name)
                    self.connected = False
                    return False

                self.device_path = self.device.path
                self.device_name = self.device.name
                self.connected = True
                logger.info("scanner_connected", manager=self.name,
                           path=self.device_path, name=self.device_name)
                return True
            except Exception as e:
                logger.error("scanner_connect_error", manager=self.name, error=str(e))
                self.connected = False
                return False

    def disconnect(self):
        """Handle scanner disconnection"""
        with self._lock:
            self.connected = False
            self.disconnect_count += 1
            self.last_disconnect_time = datetime.now().isoformat()
            logger.warning("scanner_disconnected", manager=self.name,
                          disconnect_count=self.disconnect_count,
                          device=self.device_name)

    def read_loop(self):
        """Read barcodes from scanner - runs in thread"""
        barcode = ''
        while self.running:
            if not self.connected or self.device is None:
                time.sleep(0.5)
                continue

            try:
                for event in self.device.read_loop():
                    if not self.running:
                        break
                    if not self.pause_token.is_paused:
                        if event.type == ecodes.EV_KEY:
                            eventdata = categorize(event)
                            if eventdata.keystate == 1:  # Keydown
                                scancode = eventdata.scancode
                                if scancode == 28:  # Enter
                                    if barcode:
                                        self.code_queue.put(barcode)
                                    barcode = ''
                                else:
                                    key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                                    barcode = barcode + key
            except OSError as e:
                logger.error("scanner_read_error", manager=self.name,
                            error=str(e), errno=e.errno)
                self.disconnect()
                barcode = ''
            except Exception as e:
                logger.error("scanner_unexpected_error", manager=self.name, error=str(e))
                self.disconnect()
                barcode = ''

    def start_reader(self):
        """Start the barcode reader thread"""
        if self.reader_thread is None or not self.reader_thread.is_alive():
            self.reader_thread = threading.Thread(
                target=self.read_loop,
                daemon=True,
                name=f"ScannerReader-{self.name}"
            )
            self.reader_thread.start()
            logger.info("scanner_reader_started", manager=self.name)

    def attempt_reconnect(self):
        """Attempt to reconnect to scanner"""
        if self.connected:
            return True

        logger.info("scanner_reconnect_attempt", manager=self.name,
                   attempt=self.reconnect_count + 1)

        # Need to re-create InputDevice object
        self.device = None
        if self.connect():
            self.reconnect_count += 1
            self.last_reconnect_time = datetime.now().isoformat()
            logger.info("scanner_reconnected", manager=self.name,
                       reconnect_count=self.reconnect_count,
                       device=self.device_name)
            return True
        return False

    def get_status(self):
        """Get scanner status for health reporting"""
        return {
            "connected": self.connected,
            "device_name": self.device_name or "unknown",
            "device_path": self.device_path,
            "disconnect_count": self.disconnect_count,
            "reconnect_count": self.reconnect_count,
            "last_disconnect": self.last_disconnect_time,
            "last_reconnect": self.last_reconnect_time
        }

    def show_status(self, message1, message2):
        """Show status on LCD if available"""
        if self.lcd and self.display_address:
            self.lcd.lcd_string(message1, l1, self.display_address)
            self.lcd.lcd_string(message2, l2, self.display_address)

    def stop(self):
        """Stop the scanner manager"""
        self.running = False

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
                 inputdevice,
                 gpioout,
                 name):

        self.display_address = i2cdisplayaddress
        self.input_device = inputdevice  # Now receives InputDevice object directly
        self.gpio_out = gpioout
        self.lcd = None
        self.name = name
        self.logger = logger
        self.bus = bus
        self.scanner_manager = None

    def logmessage(self, level, message):
        """logs messages to file"""
        log = getattr(logger, level)
        log(message)

    def enableGate(self):
        self.gpio_out.on()
        time.sleep(1.5)
        self.gpio_out.off()
        return True

    def checkCode(self, code: str):
        """Reboot and Shutdown codes"""
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
        """Main function"""
        ncodes = 0
        self.lcd = lcd
        print(self.lcd)
        print(self.display_address)
        fhandler = self.createFile(workingdir=workingdir, sysname=self.name)

        # Initialize scanner manager with auto-reconnect
        code_queue = queue.Queue(maxsize=1)
        self.scanner_manager = ScannerManager(
            name=self.name,
            code_queue=code_queue,
            pause_token=pauseDevice,
            lcd=lcd,
            display_address=self.display_address,
            initial_device=self.input_device if self.input_device else None
        )

        # If no initial device, try to connect
        if not self.scanner_manager.connected:
            self.scanner_manager.connect()

        if self.scanner_manager.connected:
            self.lcd.lcd_string("PISTOLA OK", l2, self.display_address)
            self.logmessage('info', f"SCANNER CONNECTED: {self.scanner_manager.device_name}")
        else:
            self.lcd.lcd_string("PISTOLA OFF", l2, self.display_address)
            self.logmessage('error', "SCANNER NOT FOUND")

        # Start scanner reader thread
        self.scanner_manager.start_reader()

        time.sleep(1)
        code = None
        nloops = 0
        FAILURE_COUNT = 5

        while True:
            jet111data = None
            marked = False

            # Check hardware restart button
            brestart = rasp_button_restart.pin.state
            if brestart == 0:
                self.lcd.lcd_string("REINICIANDO", l1, self.display_address)
                self.lcd.lcd_string("YA VOLVEMOS", l2, self.display_address)
                if fhandler is not None:
                    fhandler.close()
                self.logmessage('error', 'RESTART REQUIRED BY BUTTON')
                self.scanner_manager.stop()
                exit()

            nloops += 1

            # Read from scanner queue
            if code is None:
                if not code_queue.empty():
                    jet111data = code_queue.get()
                    if jet111data is not None:
                        self.lcd.lcd_string(f'{jet111data}', l1, self.display_address)
                        code = jet111data

            # Process scanned code
            bfinalize_job = False
            if code is not None:
                ncodes += 1
                pauseDevice.pauseDevice()
                self.checkCode(code)
                result = self.apicall(code)
                self.logmessage('info', f'{code} - {dumps(result)}')

                if result['apistatus'] == True:
                    self.lcd.lcd_string(f'{result["m1"]}', l1, self.display_address)
                    self.lcd.lcd_string(f'{result["m2"]}', l2, self.display_address)
                    if result['code'] == False:
                        time.sleep(1)
                    else:
                        marked = self.enableGate()
                        if marked:
                            self.logmessage('info', f'CODIGO MARCADO {code}')
                    ticket_string = f'code: {code}, status:{result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
                    bfinalize_job = True
                    FAILURE_COUNT = 5
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
                        FAILURE_COUNT = 5

                if bfinalize_job:
                    code = None
                    pauseDevice.resumeDevice()
                    if ncodes > 5:
                        self.lcd.initDisplay(self.display_address)
                        ncodes = 0
                if fhandler is not None:
                    fhandler.write(ticket_string)
                    fhandler.flush()
            else:
                # Idle state - show status based on scanner connection
                if self.scanner_manager.connected:
                    self.lcd.lcd_string("CARNAVAL 2026", l1, self.display_address)
                    self.lcd.lcd_string("NUEVO INGRESO", l2, self.display_address)
                # Watchdog handles "DESCONECTADA" display

                if nloops > 20:
                    self.lcd.initDisplay(self.display_address)
                    nloops = 0
                    ncodes = 0

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

def get_device_health(display_addresses=None):
    """Collect device health metrics"""
    # Aggregate scanner stats from all managers
    total_disconnects = 0
    total_reconnects = 0
    all_connected = True
    scanner_details = []

    for name, manager in scanner_managers.items():
        status = manager.get_status()
        total_disconnects += status.get('disconnect_count', 0)
        total_reconnects += status.get('reconnect_count', 0)
        if not status.get('connected', False):
            all_connected = False
        scanner_details.append({
            'name': name,
            'connected': status.get('connected', False),
            'device': status.get('device_name', 'unknown')
        })

    health = {
        "device": DEVICE_NAME,
        "ip": get_local_ip(),
        "timestamp": datetime.now().isoformat(),
        "network": {
            "connected": True,
            "server_reachable": check_server_reachable(),
            "ip_address": get_local_ip()
        },
        "scanner": {
            "connected": all_connected,
            "device_name": "dual scanners",
            "disconnect_count": total_disconnects,
            "reconnect_count": total_reconnects,
            "scanners": scanner_details
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

def scanner_watchdog_thread():
    """Monitor all scanner connections and auto-reconnect on disconnect"""
    logger.info("scanner_watchdog_started", interval=SCANNER_WATCHDOG_INTERVAL)

    was_connected = {}  # Track previous state per scanner

    while True:
        try:
            for name, manager in scanner_managers.items():
                is_connected = manager.connected
                prev_connected = was_connected.get(name, True)

                # Detect disconnection
                if prev_connected and not is_connected:
                    logger.warning("scanner_watchdog_detected_disconnect", scanner=name)
                    manager.show_status("PISTOLA", "RECONECTANDO...")

                # Attempt reconnection if disconnected
                if not is_connected:
                    logger.info("scanner_watchdog_attempting_reconnect", scanner=name)
                    time.sleep(SCANNER_RECONNECT_DELAY)

                    if manager.attempt_reconnect():
                        manager.show_status("PISTOLA", "RECONECTADA OK")
                        time.sleep(2)
                    else:
                        manager.show_status("PISTOLA", "NO DETECTADA")

                was_connected[name] = manager.connected

        except Exception as e:
            logger.error("scanner_watchdog_error", error=str(e))

        time.sleep(SCANNER_WATCHDOG_INTERVAL)

def health_reporter_thread(interval=HEALTH_REPORT_INTERVAL, display_addresses=None):
    """Background thread that reports health every N seconds"""
    logger.info("health_reporter_started", interval=interval)
    while True:
        try:
            health = get_device_health(display_addresses=display_addresses)
            post(f"{DASHBOARD_URL}/api/health", json=health, timeout=5)
            logger.info("health_reported", device=DEVICE_NAME,
                       cpu=health["system"].get("cpu_percent"),
                       scanners_connected=health["scanner"].get("connected"))
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

    # Start scanner watchdog thread (monitors all scanners)
    threading.Thread(
        target=scanner_watchdog_thread,
        daemon=True,
        name="ScannerWatchdog"
    ).start()

    # Start health reporter thread
    display_addresses_list = [display_addressa, display_addressb]
    threading.Thread(
        target=health_reporter_thread,
        args=(HEALTH_REPORT_INTERVAL, display_addresses_list),
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

    logger.info("monitoring_threads_started",
               health_interval=HEALTH_REPORT_INTERVAL,
               command_interval=COMMAND_POLL_INTERVAL,
               watchdog_interval=SCANNER_WATCHDOG_INTERVAL)

    # Detect available scanners
    idevs = getInputDevices()
    logger.info("scanners_detected", count=len(idevs),
               devices=[d.name for d in idevs])

    # Setup dual access systems
    if len(idevs) >= 2:
        asys = {
            "Proveedores1": {"gpio_out": relay_outa, "display_i2caddress": 0x27, "input_device": idevs[0]},
            "Proveedores2": {"gpio_out": relay_outb, "display_i2caddress": 0x26, "input_device": idevs[1]}
        }
    elif len(idevs) == 1:
        logger.warning("only_one_scanner_detected")
        lcd.lcd_string("SOLO 1 PISTOLA", l1, display_addressa)
        asys = {
            "Proveedores1": {"gpio_out": relay_outa, "display_i2caddress": 0x27, "input_device": idevs[0]},
            "Proveedores2": {"gpio_out": relay_outb, "display_i2caddress": 0x26, "input_device": None}
        }
    else:
        logger.error("no_scanners_detected")
        lcd.lcd_string("NO PISTOLAS", l1, display_addressa)
        lcd.lcd_string("VERIFICAR USB", l2, display_addressa)
        asys = {
            "Proveedores1": {"gpio_out": relay_outa, "display_i2caddress": 0x27, "input_device": None},
            "Proveedores2": {"gpio_out": relay_outb, "display_i2caddress": 0x26, "input_device": None}
        }

    # Create and start access systems
    asA = AccessSystem(
        name="Proveedores1",
        i2cdisplayaddress=asys['Proveedores1']["display_i2caddress"],
        inputdevice=asys['Proveedores1']["input_device"],
        gpioout=asys['Proveedores1']['gpio_out']
    )
    threading.Thread(target=asA.main, args=(lcd,), daemon=True).start()

    asB = AccessSystem(
        name="Proveedores2",
        i2cdisplayaddress=asys['Proveedores2']["display_i2caddress"],
        inputdevice=asys['Proveedores2']["input_device"],
        gpioout=asys['Proveedores2']['gpio_out']
    )
    threading.Thread(target=asB.main, args=(lcd,), daemon=True).start()

    logger.info("access_systems_started", systems=["Proveedores1", "Proveedores2"])

    # Main loop - keep alive
    while True:
        time.sleep(10)