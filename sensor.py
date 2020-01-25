#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import logging
import argparse
import os


# Command line arguments
parser = argparse.ArgumentParser(description='PIR motion sensor script for keeping screen on and off')
parser.add_argument("-t", default=300, metavar='seconds', type=int, help="Time before screen goes off, default: 300 seconds")
parser.add_argument("-p", default=16, metavar='pin_number', type=int, help="Pin used to collect motion sensor data, default: 16")
parser.add_argument("-o", required=True, metavar='on_command', help="Execute for when moved detected")
parser.add_argument("-f", required=True, metavar='off_command', help="Execute after timeout")

args = parser.parse_args()
timeUntilScreenOff = args.t
pirPin = args.p
cmdOn = args.o
cmdOff = args.f

# Prepare logger
logger = logging.getLogger('Sensor')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(3, GPIO.OUT)

timer = 0
previousState = 0
screenOn = True

while True:
    state = GPIO.input(pirPin)

    if state == 1:
        if previousState == 0:
            if timer > 0:
                logger.info('Motion detected, timer reset')
                timer = 0
            if not screenOn:
                logger.info('Execute ON')
                screenOn = True
                os.system(cmdOn)
                # execute cli screen on
    elif state == 0 and timer < timeUntilScreenOff:
        timer = timer + 1
        logger.debug('Timer running ' + str(timer) + ' sec')

        if timer == timeUntilScreenOff:
            logger.info('Timer reached ' + str(timer) + ' seconds')
            if screenOn:
                logger.info('Execute OFF')
                screenOn = False
                os.system(cmdOff)

    previousState = state

    time.sleep(1)
