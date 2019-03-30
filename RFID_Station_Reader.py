#!/usr/bin/env python

import RPi.GPIO as GPIO
import rfid.SimpleMFRC522 as SimpleMFRC522
import netifaces
import time
import sys
import threading
from blth.PyBluezClient import Client

class RFIDReader(object):
	
	def __init__(self):
		self.reader = SimpleMFRC522.SimpleMFRC522()
		self.station_id = str(netifaces.ifaddresses('wlan0')[netifaces.AF_LINK][0]['addr'])
		self.status = "open"
		self.red_pin = 11 
		self.green_pin = 12
		print("[RFID Reader Initialized]")
		print "[Station Id]", self.station_id
	
	def turnOn(pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
	
	def turnOff(pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
	
	def changeIndicator(self):
		if self.status == 'open':	
			self.turnOff(self.red_pin)
			self.turnOn(self.green_pin)
		elif self.status == 'occupied':
			self.turnOff(self.green_pin)
			self.turnOn(self.red_pin)	
	
	def read(self):
		print("[RFID Reader Reading]")
		card_id, _ = self.reader.read()
		while not card_id and client.alive:
			card_id, _ = self.reader.read()
		return card_id

def read_rfid(rfid_reader, client):
	client.send(rfid_reader.station_id)
	while(client.alive):
		user_id = rfid_reader.read() 
		if user_id:
			print "[Returned RFID] " + str(user_id)
			client.send(str(user_id))
			time.sleep(2)

if __name__ == '__main__':
	try:
		rfid_reader = RFIDReader()
		client = Client()
		rfid_reader_thread = threading.Thread(target=read_rfid, args=(rfid_reader, client,))
		rfid_reader_thread.start()
		while 1:
			server_msg = client.recv()
			print "[Server Message]", server_msg
			if server_msg == "QUIT":
				client.alive = False
			elif server_msg == "occupied" or server_msg == "open":
				if server_msg != rfid_reader.status:
					rfid_reader.status = server_msg
					rfid_reader.changeIndicator()
				#rfid_reader.status = server_msg

	except:
		client.alive = False
		client.close()
	finally:
		GPIO.cleanup()

