"""Batak game, maximum light switch off in 60 seconds"""
import random
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

BUTTONS = [6, 13, 19, 26]
LEDS = [12, 16, 20, 21]

def test():
    """Light led if button on"""
    while True:
        for i, button in enumerate(BUTTONS):
            if GPIO.input(button):
                GPIO.output(LEDS[i], 0)
            else:
                GPIO.output(LEDS[i], 1)
        time.sleep(0.05)

def game():
    """One 60 seconds game"""
    target = random.randint(0, len(LEDS))
    score = 0
    GPIO.output(LEDS[target], 1)
    start = time.time()
    while time.time() - start < 60:
        found = -1
        for i, button in enumerate(BUTTONS):
            if not GPIO.input(button):
                # button down is 0
                if found == -1:
                    found = i
                else:
                    found = 10000
        if found == target:
            #GOOD!
            score += 1
            GPIO.output(LEDS[target], 0)
            newtarget = random.randint(0, len(LEDS))
            while newtarget == target:
                newtarget = random.randint(0, len(LEDS))
            target = newtarget
            GPIO.output(LEDS[target], 1)
        else:
            time.sleep(0.05)
    GPIO.output(LEDS[target], 0)
    return score

def main():
    """Batak game, maximum light switch off in 60 seconds"""
    for button in BUTTONS:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for led in LEDS:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 0)

    try:
        time.sleep(10)
        print("Game started")
        score = game()
        print("Your score is", score)
    except KeyboardInterrupt:
        print("Stop and cleanup")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
