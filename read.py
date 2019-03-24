#!/usr/bin/env python

import RPi.GPIO as GPIO
import rfid.SimpleMFRC522 as SimpleMFRC522
import time
import sys
import threading
from blth.PyBluezClient import Client

class RFIDReader(object):
	
	def __init__(self):
		self.reader = SimpleMFRC522.SimpleMFRC522()
		self.USERS = {
			584188316561: "Salman Mithani",
			584191865972: "Amanda Bsaibes",
			584191477388: "Nick Tiner",
			584186490074: "Blake Nelson",
			550290760921L: "Michelle",
			1007720083112L: "Katherine",
			571141398222L: "Nadia",
			636626148947L: "Arthur",
			620855075937L: "Sandy",
			552941823103L: "Bella",
			804062891361L: "Alpha",
			864205562678L: "Beta",
			460750851524L: "Gamma",
			50765237519L: "Delta",
			1058314478472L: "Epsilon",
			256152243528L: "Zeta",
			621300902457L: "Eta",
			276112974647: "Example"
		}
		print("Initialized RFID reader")
	
	def read(self):
		print("Reading from reader...")
		card_id, _ = self.reader.read()
		while not card_id and client_alive:
			card_id, _ = self.reader.read()
		user_name = self.USERS[card_id] if card_id in self.USERS else 'UNKNOWN'
			
		print("Returning ID")
		return card_id, user_name
		
	def addUser(self):
		while(1):
			card_id, _ = self.reader.read()
			if card_id:				
				print("User Id is... " + str(card_id))
				if card_id in self.USERS:
					print("Are you sure you want to replace " + self.USERS[card_id] + " ? (Y/N)")
					replace = raw_input()
					if replace.upper() == "N":
						return
				print("Enter new username: ")
				user_name = raw_input()
				self.USERS[card_id] = user_name
				break

def rfid_reader(card_reader):
	while(client_alive):
		user_id, user_name = card_reader.read() 
		if user_id:
			print(user_name, user_id)
			client.send(user_id)
			time.sleep(1.5)
	
client_alive = True
if __name__ == '__main__':
	
	try:
		card_reader = RFIDReader()
		client = Client()
		rfid_reader_thread = threading.Thread(target=rfid_reader, args=(card_reader, ))
		rfid_reader_thread.start()
		while 1:
			server_msg = client.recv()
			print("Message from the server is", server_msg)
			if(server_msg == "QUIT"):
				print("in the if statement")
				client_alive = False
				#rfid_reader_thread.exit()
				#sys.exit()
		
		#~ time.sleep(2)
		#~ print("Ready to add/replace a user")
		#~ card_reader.addUser()
		#~ time.sleep(2)
		#~ print("Read to read a user again")
		#~ while(1):
			#~ user_id, user_name = card_reader.read()
			#~ if user_id:
				#~ print(user_name, user_id)
				#~ client.send(user_id)
				#~ break
			#~ else:
				#~ print("U suck")		
	except:
		client_alive = False
		client.close()
	finally:
		GPIO.cleanup()
