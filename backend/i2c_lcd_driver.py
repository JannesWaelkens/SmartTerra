#!/usr/bin/python
#  https://raspberrytips.nl/lcd-scherm-20x4-i2c-raspberry-pi/

import sys
import smbus
import time
import datetime
import subprocess

I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 20  # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On 0X08 / Off 0x00

ENABLE = 0b00000100  # Enable bit

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


class I2c_led_driver():
    def __init__(self):
        self.statusip()

    def lcd_init(self):
        self.lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):

        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        bus.write_byte(I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        bus.write_byte(I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(E_DELAY)
        bus.write_byte(I2C_ADDR, (bits | ENABLE))
        time.sleep(E_PULSE)
        bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):

        message = message.ljust(LCD_WIDTH, " ")

        self.lcd_byte(line, LCD_CMD)

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def statusip(self):
        self.lcd_init()
        # adressen ophalen van de pi
        ips = subprocess.check_output(['hostname', '--all-ip-addresses'])
        ips = ips.decode()
        ips = ips.split(" ")
        # \n verwijderen
        del ips[-1]
        # is = str(ips)

        if (ips[0] == '169.254.10.1'):
            self.lcd_string("IP:{}".format(ips[1]), LCD_LINE_4)
        else:
            self.lcd_string("IP:{}".format(ips[0]), LCD_LINE_4)

    def statusip1(self):
        # adressen ophalen van de pi
        ips = subprocess.check_output(['hostname', '--all-ip-addresses'])
        ips = ips.decode()
        ips = ips.split(" ")
        # \n verwijderen
        del ips[-1]
        # ips = str(ips)

        if (ips[0] == '169.254.10.1'):
            self.lcd_string("IP:{}".format(ips[1]), LCD_LINE_4)
        else:
            self.lcd_string("IP:{}".format(ips[0]), LCD_LINE_4)

    def main(self, temperatuur):
        # try:
        self.lcd_init()
        self.lcd_string("SmartTerra by Jannes", LCD_LINE_1)
        self.lcd_string(("Het is %s graden" % temperatuur), LCD_LINE_2)
        # self.lcd_string(("De deur is %s"% toestanddeur), LCD_LINE_3)
        self.statusip1()
        # time.sleep(5)
    # finally:
    #     self.lcd_byte(0x01,LCD_CMD)
