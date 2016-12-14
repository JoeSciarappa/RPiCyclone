#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import random 
import datetime
import logging
import atexit
import signal
import sys
import os
import math

##Logging 
logger = logging.getLogger('A4 Cyclone')
hdlr = logging.FileHandler('/var/log/cyclone.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
##Set logging Level
#Options include: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger.setLevel(logging.CRITICAL)


##Stop bothering me with GPIO warnings I do not care about
GPIO.setwarnings(False) 

##Initiate board 
GPIO.setmode(GPIO.BOARD)

##Initiate pins
#Left
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

#Center
GPIO.setup(18, GPIO.OUT)

#Right
GPIO.setup(16, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

#Button
GPIO.setup(13, GPIO.IN)


##Functions 
def win(seed):
	ascii('winner.txt')
        #Point range 1 to 1681 depending on seed value
        points = math.pow((66 - int(seed)),2)
        logger.critical("Points Received: " + str(points))

	for x in range(10):
        	GPIO.output(18, GPIO.HIGH)
                time.sleep(.2)
                GPIO.output(18, GPIO.LOW)
		time.sleep(.2)

def lose():
	ascii('loser.txt')
	for x in range(10):
                GPIO.output(11, GPIO.HIGH)
                GPIO.output(36, GPIO.HIGH)
                time.sleep(.2)
                GPIO.output(11, GPIO.LOW)
		GPIO.output(36, GPIO.LOW)
                time.sleep(.2)

def check(pin,seed):
	if GPIO.input(13) == True:	
		logger.debug("Game should stop")
                time.sleep(.5)
		logger.debug("Turning pin " +str(pin) + " off")
                GPIO.output(pin, GPIO.LOW)
		if pin == 18:
			win(seed)
			main()
		else:
			lose()
			main()
	else:
		logger.debug("Game should continue")
          
def ascii(art):
	art = os.path.join(os.path.dirname(__file__), art)
	with open(art) as f:
		for line in f:
                	logger.critical(line.rstrip())
	

 
def light(pin, seed):
	logger.debug("Turning pin " + str(pin) + " on")
	GPIO.output(pin, GPIO.HIGH )
	logger.debug("Sleeping for " + str(seed) + " milliseconds")
	time.sleep(seed / 1000.0) 
	logger.debug("Checking if game should stop")
	check(pin,seed)
	logger.debug("Turning pin " + str(pin) + " off")
	GPIO.output(pin, GPIO.LOW)
	
def cleanup(signal, frame):
	logger.info("Exit detected - Cleaing up")
	logger.debug("Recieved Signal" + str(signal) + " on frame " + str(frame) )
	GPIO.cleanup()
	sys.exit(0)

def main():
	
	#Exit Detection
	atexit.register(cleanup)
	signal.signal(signal.SIGTERM,cleanup)
	

	logger.info("Cyclone game Started")

	try:
		while True:

			if GPIO.input(13) == False:
	
				#Pull in random seed for tempo
				seed=random.randrange(25, 65, 1)
				logger.info("Using seed value " +str(seed))
 
				while GPIO.input(13) == False:
	
					try:
	
						light(11,seed)
						light(15,seed)
						light(29,seed)
						light(33,seed)
						light(18,seed)
						light(36,seed)
						light(32,seed)
						light(22,seed)
						light(16,seed)

					except Exception as e: 
						logger.critical("----Critical Hit----")	
						logger.critical(str(e))
						logger.critical("--------------------")
	except Exception as e:
		logger.critical("----Critical Hit----")
		logger.critical(str(e))
		logger.critical("--------------------")

#Run this shit
if __name__ == '__main__':
	main()

