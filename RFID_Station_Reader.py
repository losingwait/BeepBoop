#!/usr/bin/env python

import RPi.GPIO as GPIO
import rfid.SimpleMFRC522 as SimpleMFRC522
import time
import sys
import re, uuid
import threading
from blth.PyBluezClient import Client

class RFIDReader(object):
	
	def __init__(self):
		self.reader = SimpleMFRC522.SimpleMFRC522()
		self.station_id = ':'.join(re.findall('..', '%012x' % uuid.getnode())).encode()
		print("[RFID Reader Initialized]")
		print "[Station Id]", self.station_id
	def read(self):
		print("[RFID Reader Reading]")
		card_id, _ = self.reader.read()
		while not card_id and client_alive:
			card_id, _ = self.reader.read()
		return card_id

def read_rfid(rfid_reader, client):
	while(client_alive):
		user_id = rfid_reader.read() 
		if user_id:
			print "[Returned RFID] " + str(user_id)
			client.send(str(user_id) + "|" + rfid_reader.station_id)
			time.sleep(2)
	
client_alive = True

if __name__ == '__main__':
	
	try:
		rfid_reader = RFIDReader()
		client = Client()
		rfid_reader_thread = threading.Thread(target=read_rfid, args=(rfid_reader, client,))
		rfid_reader_thread.start()
		while 1:
			server_msg = client.recv()
			print "[Server Message]", server_msg
			if(server_msg == "QUIT"):
				client_alive = False
	except:
		client_alive = False
		client.close()
	finally:
		GPIO.cleanup()

