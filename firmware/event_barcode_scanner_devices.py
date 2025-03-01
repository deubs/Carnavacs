from evdev import InputDevice, categorize, ecodes, list_devices
import threading

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
			# break
	return inputdevs


def readBarCodes(device):
	barcode = ''
	try:
		for event in device.read_loop():
			if event.type == ecodes.EV_KEY:
				eventdata = categorize(event)
				if eventdata.keystate == 1: # Keydown
					scancode = eventdata.scancode
					if scancode == 28: # Enter
						print(f'{device.name} {barcode}')
						barcode = ""	
					else:
						key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
						barcode = barcode + key
						if key == NOT_RECOGNIZED_KEY:
							print('unknown key, scancode=' + str(scancode))
	except Exception as e:
		print(e)


inputdevs = getInputDevices()
devices = []
for indev in inputdevs:
	print(indev.name)
	print(indev.path)
	device = InputDevice(indev)
	threading.Thread(target = readBarCodes, args = (device, ), daemon = True).start()

nthreads = threading.enumerate() 
print(nthreads)

while True:
	if threading.enumerate() == nthreads:
		continue
	else:
		print("Thread has stopped. Exit")
		exit()
