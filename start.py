import board
import random
import sys
import time

from adafruit_ht16k33.segments import BigSeg7x4

def start(display):
    time.sleep(1)
    display.print("   0")
    time.sleep(1)
    display.print("  00")
    time.sleep(1)
    display.print(" 000")
    time.sleep(1)
    display.print("0000")
    time.sleep(random.randint(10, 40)/10)
    display.fill(0)

def play(display):
    long = 30
    start = time.time()
    while time.time() - start < long:
        remaining = long - int(time.time() - start)
        display.print(f'  {remaining:02}')
        time.sleep(0.05)
    display.blink_rate = 1
    display.print("  00")
    time.sleep(3)
    display.fill(0)
    display.blink_rate = 0

def main():
    i2c = board.I2C()
    display1 = BigSeg7x4(i2c, address=0x71)
    display2 = BigSeg7x4(i2c, address=0x70)
    display1.brightness = 0.2
    display2.brightness = 0.2
    display1.fill(0)
    display2.fill(0)
    start(display2)
    play(display1)

if __name__ == "__main__":
    main()
