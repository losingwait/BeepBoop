#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

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
	
	def read(self):
		card_id, _ = self.reader.read()
		user_name = self.USERS[card_id] if card_id in self.USERS else 'UNKNOWN'
			
		return card_id, user_name
	
	
if __name__ == '__main__':
	
	card_reader = RFIDReader()
	
	try:
		while(1):
			user_id, user_name = card_reader.read()
			if user_id:
				print(user_name)
				break
	finally:
		GPIO.cleanup()
