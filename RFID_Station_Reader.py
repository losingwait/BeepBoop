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
		self.blue_pin = 13
		#~ self.turnOn(self.)
		print("[RFID Reader Initialized]")
		print "[Station Id]", self.station_id
		GPIO.cleanup()
	
	def turnOn(self, pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
	
	def turnOff(self, pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
	
	def changeIndicator(self):
		if self.status == 'open':	
			self.turnOff(self.red_pin)
			self.turnOff(self.blue_pin)
			self.turnOn(self.green_pin)
		elif self.status == 'occupied':
			self.turnOff(self.green_pin)
			self.turnOff(self.blue_pin)
			self.turnOn(self.red_pin)
		elif self.status == 'queued':
			self.turnOff(self.green_pin)
			self.turnOff(self.read_pin)
			self.turnOn(self.blue_pin)	
			
	def blink_red(self):
		self.turnOff(self.blue_pin)
		for i in range 5:
			self.turnOn(self.red_pin)
			time.sleep(.2)
			self.turnOff(self.red_pin)
			time.sleep(.2)
		self.changeIndicator()		
	
	def read(self):
		print("[RFID Reader Reading]")
		card_id, _ = self.reader.read()
		while not card_id and client.alive:
			card_id, _ = self.reader.read()
		return card_id

server_msg = None


def read_rfid(rfid_reader, client):
	client.send(rfid_reader.station_id)
	#~ ready_read = True
	while(client.alive):
		if(client.ready_read):
			user_id = rfid_reader.read() 
			if user_id:
				print "[Returned RFID] " + str(user_id)
				client.send(str(user_id))
				client.ready_read = False
			
if __name__ == '__main__':
	client = None
	try:
		#~ ready_read = True
		rfid_reader = RFIDReader()
		client = Client()
		rfid_reader_thread = threading.Thread(target=read_rfid, args=(rfid_reader, client,))
		rfid_reader_thread.start()
		rfid_reader.changeIndicator()
		while 1:
			server_msg = client.recv()
			print "[Server Message]", server_msg
			if server_msg == "QUIT":
				client.alive = False
				break;
			location, server_msg = server_msg.split("|")
			if location is "R":
				client.ready_read = True
			
			if server_msg == "occupied" or server_msg == "open" or server_msg == "queued":
				if server_msg != rfid_reader.status:
					rfid_reader.status = server_msg
					rfid_reader.changeIndicator()
			elif server_msg == "denied"
				rfid_reader.blink_red()

	except Exception, e:
		print('in except statement ' + str(e))
		if client:
			client.alive = False
			client.close()
	finally:
		GPIO.cleanup()

