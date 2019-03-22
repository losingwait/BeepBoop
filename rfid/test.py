#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

GPIO.cleanup()
print("Starting RFID pls...")
reader = SimpleMFRC522.SimpleMFRC522()

try:
        print("Before reading...")
	id, text = reader.read()
	print(id)
        print("...after reading")
	
finally:
	GPIO.cleanup()
