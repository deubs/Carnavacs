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

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
E_WRITE_DELAY = 0.001
#Open I2C interface
print(f'NODE: {platform.node()}')
bus = smbus.SMBus(1)  # Rev 1 Pi uses 0

class LCD(object):
  
    def lcd_init(self, i2caddressa, i2caddressb):
        self.i2caddressa = i2caddressa
        self.i2caddressb = i2caddressb
    # Initialise displays
        self.initDisplay(self.i2caddressa)
        self.initDisplay(self.i2caddressb)
        time.sleep(E_DELAY)


    def initDisplay(self, addr):
        print(f'begin init display with address {hex(addr)}')
        self.lcd_byte(0x33, LCD_CMD, addr) # 110011 Initialise
        self.lcd_byte(0x32, LCD_CMD, addr) # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD, addr) # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD, addr) # 001100 Display On,Cursor Off, Blink Off 
        self.lcd_byte(0x28, LCD_CMD, addr) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD, addr) # 000001 Clear display
        print(f'finish init display with address {hex(addr)}')


    def lcd_byte(self, bits, mode, addr):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        try:
            bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
            bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
            # High bits
            bus.write_byte(addr, bits_high)
            self.lcd_toggle_enable(bits_high, addr)
            # Low bits
            bus.write_byte(addr, bits_low)
            self.lcd_toggle_enable(bits_low, addr)
        except Exception as e:
            print(e)
            self.initDisplay(addr)


    def lcd_toggle_enable(self, bits, addr):
    # Toggle enable
        time.sleep(E_DELAY)
        bus.write_byte(addr, (bits | ENABLE))
        time.sleep(E_PULSE)
        bus.write_byte(addr, (bits & ~ENABLE))
        time.sleep(E_DELAY)


    def lcd_clear(self, addr):
        self.lcd_byte(0x01, LCD_CMD, addr) # 000001 Clear display


    def lcd_string(self, message, line, addr):
        # Send string to display
        message = message.ljust(LCD_WIDTH," ")
        self.lcd_byte(line, LCD_CMD, addr)
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR, addr)


    def main(self, addra, addrb):
    # Initialise display
        self.lcd_init(addra, addrb)
        while True:
            # Send some test
            self.lcd_string("RPiSpy         <", LCD_LINE_1, addra)
            self.lcd_string("I2C LCD        <", LCD_LINE_2, addrb)
            time.sleep(3)        
            # Send some more text
            self.lcd_string(">         RPiSpy", LCD_LINE_1, addrb)
            self.lcd_string(">        I2C LCD", LCD_LINE_2, addra)
            time.sleep(3)


if __name__ == '__main__':
    i2caddressa = 0x27
    i2caddressb = 0x26
    lcd = LCD()
    try:
        lcd.main(i2caddressa, i2caddressb)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x01, LCD_CMD, i2caddressa)
        lcd.lcd_byte(0x01, LCD_CMD, i2caddressb)