"""
$ sudo pip install rpi.gpio
"""

import RPi.GPIO as GPIO

Sw_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(Sw_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def switch_state():
    if (GPIO.input(Sw_pin) == 0) :
        return 1
    else :
        return 0

