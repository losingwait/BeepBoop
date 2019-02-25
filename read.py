#!/usr/bin/env python

import RPi.GPIO as GPIO
import rfid.SimpleMFRC522 as SimpleMFRC522
from blth.PyBluezClient import Client

class RFIDReader(object):
	
	def __init__(self):
		self.reader = SimpleMFRC522.SimpleMFRC522()
		self.USERS = {
			584188316561: "Salman Mithani",
			584191865972: "Amanda Bsaibes",
			584191477388: "Nick tiner",
			584186490074: "Blake Nelson",
			276112974647: "example"
		}
		print("Initialized RFID reader")
	
	def read(self):
		print("Reading from reader...")
		card_id, _ = self.reader.read()
		user_name = self.USERS[card_id] if card_id in self.USERS else 'UNKNOWN'
			
		print("Returning ID")
		return card_id, user_name
	
	
if __name__ == '__main__':
	
	card_reader = RFIDReader()
	#client = Client()
	try:
		while(1):
			user_id, user_name = card_reader.read()
			if user_id:
				print(user_name, user_id)
	#			client.send(user_id)
				break
			else:
				print("U suck")
	finally:
		GPIO.cleanup()
