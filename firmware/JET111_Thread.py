#!/usr/bin/python
#--------------------------------------
#  JET111.py 
#  Author: Emiliano Melchiori
#  Date: 29/11/2024
# 
#  NexuPOS JET 111 bar code scanner. Object model

from evdev import InputDevice, categorize, ecodes, list_devices
from datetime import datetime
import calendar
import pdb
import threading
import queue

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

print(scancodes)
NOT_RECOGNIZED_KEY = u'X'

def detectDevice():
    devices = [InputDevice(path) for path in list_devices()]
    inputdev = None
    print(devices)
    for device in devices:
        print(device.name)
        if ("IMAGER 2D" in device.name) or \
            ("BF SCAN SCAN KEYBOARD" in device.name) or \
                ("NT USB Keyboard" in device.name) or \
                    ("ZKRFID R400" in device.name):

            inputdev = device.path
            break
    return inputdev
    
def connectDevice(inputdev):
    try:           
        device = InputDevice(inputdev) # Replace with your device
    except Exception as e:
        print(e)
        return None
    else:
        print(device)
        print(device.capabilities())
        return device

def saveBarcode(bc):
    d = datetime.now()
    unixtime = calendar.timegm(d.utctimetuple())	
    entry = str(unixtime) + ' ' + bc +  '\n'
    try:
        with open('barcodes.txt', 'a') as bc_file:
            bc_file.write(entry)
    except Exception as e:
        print(e)


def readBarCodes(device, q: queue):
    print('begin reading...')
    barcode = ''
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            eventdata = categorize(event)
            if eventdata.keystate == 1: # Keydown
                scancode = eventdata.scancode
                if scancode == 28: # Enter
                    saveBarcode(barcode)
                    q.put(barcode)
                    barcode = ''
                else:
                    key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                    barcode = barcode + key
                    if key == NOT_RECOGNIZED_KEY:
                        print('unknown key, scancode=' + str(scancode))


if __name__ == "__main__":
    q =  queue.Queue()
    idev = detectDevice()
    if idev is not None:
        dev = connectDevice(idev)
        threading.Thread(target = readBarCodes, args = (dev, q,), daemon = True).start()
        while True:
            bc = q.get()
            print("barcode: " + bc)
    else: 
        print("No Device Found")