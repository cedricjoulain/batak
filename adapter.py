"""Platform dependent code"""
from sys import platform

if platform == "darwin":
    # OS X
    #Mock GPIO
    class MyGPIO:
        def __init__(self):
            """mock const"""
            self.BCM = 1
            self.IN = 2
            self.OUT = 3
            self.PUD_UP = 4

        def setmode(self, mode):
            """mock setmode"""
            return

        def setup(self, gpio, inout, pull_up_down=None):
            """mock setup"""
            return

        def output(self, gpio, value):
            """mock output"""
            return

        def input(self, gpio):
            """mock output"""
            return False

        def cleanup(self):
            """mock cleanup"""
            return

    GPIO = MyGPIO()
else:
    import RPi.GPIO as GPIO

