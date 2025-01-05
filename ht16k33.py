import board
import sys
import time
from adafruit_ht16k33.segments import BigSeg7x4

i2c = board.I2C()
display = BigSeg7x4(i2c, address=0x71)
display.brightness = 0.2
display.fill(0)
sys.exit(0)
text = "NOLAN"
padd = (int(len(text) / 4)+1)*4
count = 0
while True:
    start = count % padd
    for d in range(0, 4):
        index = (start + d) % padd
        if index < len(text):
            c = text[index]
        else:
            c = " "
        display[d] = c
    time.sleep(0.2)
    count += 1
