"""Batak game, maximum light switch off in 60 seconds"""
import random
import time

import RPi.GPIO as GPIO

import const

GPIO.setmode(GPIO.BCM)

def test():
    """Light led if button on"""
    while True:
        for i, button in enumerate(const.BUTTONS):
            if GPIO.input(button):
                GPIO.output(const.LEDS[i], 0)
            else:
                GPIO.output(const.LEDS[i], 1)
        time.sleep(0.05)

def game():
    """One 60 seconds game"""
    target = random.randint(0, len(const.LEDS)-1)
    score = 0
    GPIO.output(const.LEDS[target], 1)
    start = time.time()
    while time.time() - start < 60:
        found = -1
        for i, button in enumerate(const.BUTTONS):
            if not GPIO.input(button):
                # button down is 0
                if found == -1:
                    found = i
                else:
                    found = 10000
        if found == target:
            #GOOD!
            score += 1
            GPIO.output(const.LEDS[target], 0)
            newtarget = random.randint(0, len(const.LEDS)-1)
            while newtarget == target:
                newtarget = random.randint(0, len(const.LEDS)-1)
            target = newtarget
            GPIO.output(const.LEDS[target], 1)
        else:
            time.sleep(0.05)
    GPIO.output(const.LEDS[target], 0)
    return score

def main():
    """Batak game, maximum light switch off in 60 seconds"""
    for button in const.BUTTONS:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for led in const.LEDS:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 0)

    try:
        print("Start game in 10 seconds")
        time.sleep(10)
        print("Game started")
        score = game()
        print("Your score is", score)
    except KeyboardInterrupt:
        print("Stop and cleanup")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
