import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

buttons = [6, 13, 19, 26]
leds = [12, 16, 20, 21]


for i, button in enumerate(buttons):
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for i, led in enumerate(leds):
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, 0)

try:
    while True:
        for i, button in enumerate(buttons):
            if GPIO.input(button):
                GPIO.output(leds[i], 0)
            else:
                GPIO.output(leds[i], 1)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Stop and cleanup")
    GPIO.cleanup()