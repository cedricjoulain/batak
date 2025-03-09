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

    class MyDisplay():
        """Mock 7 leds right.left displays"""
        def __init__(self, indent):
            self.indent = indent
        
        def print(self, str):
            print(self.indent, str)

    GPIO = MyGPIO()
    def get_displays():
        return MyDisplay(""), MyDisplay("     ")

else:
    import RPi.GPIO as GPIO
    import board
    from adafruit_ht16k33.segments import BigSeg7x4

    def get_displays():
        """Returns the 2 x 4 x 7 leds displays"""
        i2c = board.I2C()
        display1 = BigSeg7x4(i2c, address=0x71)
        display2 = BigSeg7x4(i2c, address=0x70)
        display1.brightness = 0.2
        display2.brightness = 0.2
        display1.fill(0)
        display2.fill(0)
        return display1, display2
