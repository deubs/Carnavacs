
#!/usr/bin/env python
"""Read button.


implements reboots through gpio button.
code from:
    https://forum.armbian.com/topic/12843-shut-down-opi-zero-using-a-push-button-on-gpio/
    by @martinayotte



Make gpio input and enable pull-up resistor.
"""

import os
import sys
import time
import logging

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port


button = port.PA10

"""Init gpio module"""
gpio.init()

"""Set directions"""
gpio.setcfg(button, gpio.INPUT)

"""Enable pullup resistor"""
gpio.pullup(button, gpio.PULLUP)
#gpio.pullup(button, gpio.PULLDOWN)     # Optionally you can use pull-down resistor


try:
    while True:
        state = gpio.input(button)      # Read button state
#        print (state)
        if state == 0:
            print("button pressed")
            logging.info("button pressed")
        time.sleep(0.2)

except KeyboardInterrupt:
    print ("Goodbye.")
  
