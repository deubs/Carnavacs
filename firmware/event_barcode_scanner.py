from evdev import InputDevice, categorize, ecodes, list_devices
from datetime import datetime
import calendar
import pdb
import time

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

def getDevice():
	devices = [InputDevice(path) for path in list_devices()]
	inputdev = None
	for device in devices:
		print(device.name)
		if ("IMAGER 2D" in device.name) or \
			("BF SCAN SCAN KEYBOARD" in device.name) or \
				("NT USB Keyboard" in device.name) or \
					("ZKRFID R400" in device.name) or \
						("BARCODE SCANNER Keyboard Interface" in device.name):
			inputdev = device.path
			break
	return inputdev

inputdev = None
while inputdev == None:
	inputdev = getDevice()
	if inputdev == None:
		print("NO DEVICE FOUND")
		time.sleep(2)

try:           
	device = InputDevice(inputdev) # Replace with your device
except Exception as e:
	print(e)
	exit()

print(device)
print(device.capabilities())
barcode = ''

def saveBarcode(bc):
	d = datetime.utcnow()
	unixtime = calendar.timegm(d.utctimetuple())	
	entry = str(unixtime) + ' ' + bc +  '\n'
	print(entry)
	with open('barcodes.txt', 'a') as bc_file:
		bc_file.write(entry)

print('begin reading...')
try:
	for event in device.read_loop():
		if event.type == ecodes.EV_KEY:
			eventdata = categorize(event)
			if eventdata.keystate == 1: # Keydown
				scancode = eventdata.scancode
				if scancode == 28: # Enter
					saveBarcode(barcode)
					barcode = ''
				else:
					key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
					barcode = barcode + key
					if key == NOT_RECOGNIZED_KEY:
						print('unknown key, scancode=' + str(scancode))
except Exception as e:
	print(e)