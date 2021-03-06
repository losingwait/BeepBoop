#!/usr/bin/env python

import RPi.GPIO as GPIO
import rfid.SimpleMFRC522 as SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
	id, text = reader.read()
	print(id)
	
finally:
	GPIO.cleanup()
