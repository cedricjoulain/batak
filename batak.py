"""Batak game, maximum light switch off in TIME seconds"""
import logging
import random
import time

import const
from adapter import GPIO, get_displays

logger = logging.getLogger(__name__)
#add to previous log
logging.basicConfig(
    filename="acf1.log",
    format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

def init_io():
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

def spad(nbr):
    """int as left justified string of size 4"""
    return str(nbr).rjust(4)

def zpad(nbr):
    """int as zero pad of size 4"""
    return f"{nbr:03d}".rjust(4)

def game(display1, display2):
    """One 60 seconds game"""
    target = random.randint(0, len(const.LEDS)-1)
    score = 0
    GPIO.output(const.LEDS[target], 1)
    start = time.time()
    while time.time() - start < const.TIME:
        remaining = const.TIME - int(time.time() - start)
        display1.print(zpad(score))
        display2.print(spad(remaining))
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
    #show last
    display1.print(zpad(score))
    display2.print(spad(0))
    #turn off all lights
    for led in const.LEDS:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 0)
    #wait a little bit blinking 0 time
    time.sleep(0.5)
    display2.print(const.EMPTY)
    time.sleep(0.5)
    display2.print(spad(0))
    time.sleep(0.5)
    display2.print(const.EMPTY)
    time.sleep(0.5)
    display2.print(spad(0))
    time.sleep(0.5)
    display2.print(const.EMPTY)
    return score

def starter(display):
    """F1 still starter"""
    time.sleep(1)
    display.print("   0")
    time.sleep(1)
    display.print("  00")
    time.sleep(1)
    display.print(" 000")
    time.sleep(1)
    display.print("0000")
    time.sleep(1)
    display.fill(0)

def main():
    """Batak game, maximum light switch off in 60 seconds"""
    logger.info("Initializing inputs/outputs and displays")
    init_io()
    display1, display2 = get_displays()
    best = 0
    score = 0
    # for ever
    start = time.time()
    while True:
        try:
            #show best score
            display1.print(zpad(best))
            #Show ACF1 or current score
            if int(time.time() - start)%2 == 0:
                display2.print(const.ACF1)
            else:
                display2.print(zpad(score))
            #any button touched ???
            pressed = False
            for button in const.BUTTONS:
                if not GPIO.input(button):
                    pressed = True
            if pressed:
                #play !!!
                logger.info("Start procedure")
                display1.print(const.EMPTY)
                starter(display2)
                logger.info("Game started")
                score = game(display1, display2)
                if best > score:
                    logger.info("Your score is %d", score)
                else:
                    best = score
                    logger.info("BEST SCORE %d", score)
            else:
                #very small pause
                time.sleep(0.05)
        except KeyboardInterrupt:
            logger.info("Stop and cleanup")
            GPIO.cleanup()
            #bye bye
            return

if __name__ == "__main__":
    main()
