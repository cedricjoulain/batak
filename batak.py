"""Batak game, maximum light switch off in TIME seconds"""
import logging
import random
import time

import const
from adapter import GPIO

logger = logging.getLogger(__name__)
#add to previous log
logging.basicConfig(filename=f'acf1.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

def initIO():
    """Initialise all board input output and displays"""
    GPIO.setmode(GPIO.BCM)
    for button in const.BUTTONS:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for led in const.LEDS:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 0)

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
    while time.time() - start < const.TIME:
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
    logger.info("Initializing inputs/outputs and displays")
    initIO()

    try:
        logger.info("Start game in 10 seconds")
        time.sleep(10)
        logger.info("Game started")
        score = game()
        logger.info(f"Your score is {score}")
    except KeyboardInterrupt:
        logger.info("Stop and cleanup")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
