import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.IN)

try:
    while True:
        if GPIO.input(26):
            GPIO.output(21, 0)
        else:
            GPIO.output(21, 1)
        time.sleep(0.001)
except KeyboardInterrupt:
    GPIO.cleanup