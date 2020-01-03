#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import logging
import argparse
import os


# Command line arguments
parser = argparse.ArgumentParser(description='PIR motion sensor script for keeping screen on and off')
parser.add_argument("-t", default=300, metavar='seconds', type=int, help="Time before screen goes off")

args = parser.parse_args()
timeUntilScreenOff = args.t

# Prepare logger
logger = logging.getLogger('Sensor')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)

# Pin used for motion sensor
PIR_PIN = 16

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(3, GPIO.OUT)

timer = 0
previousState = 0
screenOn = True

while True:
    state = GPIO.input(PIR_PIN)

    if state == 1:
        if previousState == 0:
            if timer > 0:
                logger.info('Motion detected, timer reset')
                timer = 0
            if not screenOn:
                logger.info('Turn screen on')
                screenOn = True
                os.system("tvservice -p && sudo chvt 1 && sudo chvt 7")
                # execute cli screen on
    elif state == 0 and timer < timeUntilScreenOff:
        timer = timer + 1
        logger.debug('Timer running ' + str(timer) + ' sec')

        if timer == timeUntilScreenOff:
            logger.info('Timer reached ' + str(timer) + ' seconds')
            if screenOn:
                logger.info('Turn screen off')
                screenOn = False
                os.system("tvservice -o")

    previousState = state

    time.sleep(1)
