#!/usr/bin/env python

import RPi.GPIO as GPIO
import rfid.SimpleMFRC522 as SimpleMFRC522
import json
import time
import sys
import requests

class GymReader(object):
	
	def __init__(self):
		self.reader = SimpleMFRC522.SimpleMFRC522()
		self.red_pin = 11 
		self.green_pin = 12
		print("[Gym Reader Initialized]")
		GPIO.cleanup()
	
	def turnOn(self, pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
	
	def turnOff(self, pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
	
	def blink_red(self):
		for i in range(3):
			self.turnOn(self.red_pin)
			time.sleep(.2)
			self.turnOff(self.red_pin)
			time.sleep(.2)
		
	def blink_green(self):
		for i in range(3):
			self.turnOn(self.green_pin)
			time.sleep(.2)
			self.turnOff(self.green_pin)
			time.sleep(.2)
	
	def read(self):
		print("[Gym Reader Reading]")
		card_id, _ = self.reader.read()
		while not card_id:
			card_id, _ = self.reader.read()
		return card_id


# TODO: Should probably make a utility file that has functions used by Gym and Station objs
def convertJsonToDict(json_obj):
		json_string = json_obj.replace("'", "\"")
		json_dict = json.loads(json_string)
		return json_dict
			
if __name__ == '__main__':
	try:
		gym_reader = GymReader()
		while 1:
			user_id = gym_reader.read()
			print 'User Id sent to the database is: ', user_id
			response = requests.post('https://losing-wait.herokuapp.com/gym_users/checkin', data = {'rfid': user_id})
			response_dict = convertJsonToDict(response.text)
			print(response_dict)
			if response.status_code == 400:
				gym_reader.blink_red()
			else:
				gym_reader.blink_green()
	except Exception, e:
		print('in except statement ' + str(e))

	finally:
		GPIO.cleanup()

