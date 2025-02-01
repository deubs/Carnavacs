#!/usr/bin/python
#--------------------------------------
#  LCDI2C 
#  Author: Emiliano Melchiori
#  Date: 28/11/2024
# 
#  LCD test script using I2C backpack. Object model
#  Supports 16x2 and 20x4 screens.
#  Based on lcd_i2c.py by
#
# Author : Matt Hawkins
# Date   : 20/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import platform
try:
    import smbus2 as smbus
except ImportError:
    import smbus
import time

LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants      
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
print(platform.node())
# if "raspi" in platform.node():
#     bus = smbus.SMBus(1)  # Rev 1 Pi uses 0
# else:
#     bus = smbus.SMBus(3)  # Rev 1 Pi uses 0

# for device in range(128):
#     try:
#         bus.read_byte(device)
#         i2c = device
#         print(i2c)
#     except: # exception if read_byte fails
#         pass
# I2C_ADDR = i2c


from smbus2 import SMBus, i2c_msg

# Define the addresses of the two LCD displays
address1 = 0x27
address2 = 0x3F

# Define the data to be written to each display
data1 = [40, 50]  # Example data for the first display
data2 = [60, 70]  # Example data for the second display

# Create i2c_msg objects for writing to each display
write_msg1 = i2c_msg.write(address1, data1)
write_msg2 = i2c_msg.write(address2, data2)

# Perform the write operations
with SMBus(1) as bus:
    bus.i2c_rdwr(write_msg1, write_msg2)



class LCD(object):
  
    def lcd_init(self, i2caddressa, i2caddressb):
        # print(hex(i2caddress))
        self.i2caddressa = i2caddressa
        self.i2caddressb = i2caddressb
        # self.bus = bus
    # Initialise display
        self.lcd_byte(0x33,LCD_CMD, self.i2caddressa) # 110011 Initialise
        self.lcd_byte(0x32,LCD_CMD, self.i2caddressa) # 110010 Initialise
        self.lcd_byte(0x06,LCD_CMD, self.i2caddressa) # 000110 Cursor move direction
        self.lcd_byte(0x0C,LCD_CMD, self.i2caddressa) # 001100 Display On,Cursor Off, Blink Off 
        self.lcd_byte(0x28,LCD_CMD, self.i2caddressa) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,LCD_CMD, self.i2caddressa) # 000001 Clear display
        self.lcd_byte(0x33,LCD_CMD, self.i2caddressb) # 110011 Initialise
        self.lcd_byte(0x32,LCD_CMD, self.i2caddressb) # 110010 Initialise
        self.lcd_byte(0x06,LCD_CMD, self.i2caddressb) # 000110 Cursor move direction
        self.lcd_byte(0x0C,LCD_CMD, self.i2caddressb) # 001100 Display On,Cursor Off, Blink Off 
        self.lcd_byte(0x28,LCD_CMD, self.i2caddressb) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,LCD_CMD, self.i2caddressb) # 000001 Clear display

        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode, addr):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command
        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
        # High bits
        bus.write_byte(addr, bits_high)
        self.lcd_toggle_enable(bits_high, addr)
        # Low bits
        bus.write_byte(addr, bits_low)
        self.lcd_toggle_enable(bits_low, addr)


    def lcd_toggle_enable(self, bits, addr):
    # Toggle enable
        time.sleep(E_DELAY)
        bus.write_byte(addr, (bits | ENABLE))
        time.sleep(E_PULSE)
        bus.write_byte(addr, (bits & ~ENABLE))
        time.sleep(E_DELAY)


    def lcd_string(self, message, line, addr):
    # Send string to display
        message = message.ljust(LCD_WIDTH," ")
        
        self.lcd_byte(line, LCD_CMD, addr)
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]),LCD_CHR)


    def main(self, address):
    # Initialise display
        self.lcd_init(address)
        while True:
            # Send some test
            self.lcd_string("RPiSpy         <",LCD_LINE_1)
            self.lcd_string("I2C LCD        <",LCD_LINE_2)
            time.sleep(3)        
            # Send some more text
            self.lcd_string(">         RPiSpy",LCD_LINE_1)
            self.lcd_string(">        I2C LCD",LCD_LINE_2)
            time.sleep(3)


if __name__ == '__main__':
    # i2caddress = 0x27
    lcd = LCD()
    try:
        lcd.main(I2C_ADDR)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x01, LCD_CMD)

