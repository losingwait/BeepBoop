import time
import os
import threading
import RPi.GPIO as GPIO
import netifaces
import requests
import sys
sys.path.append('..')
from blth.PyBluezClient import Client

class FreeWeightSensor(object):
	def __init__(self, clk, d_out, d_in, cs, identifier):
		self.status = "open"
		self.station_id = str(netifaces.ifaddresses('wlan0')[netifaces.AF_LINK][0]['addr']) 
		self.identifier = identifier
		GPIO.setmode(GPIO.BCM)
		DEBUG = 1
		# Port Numbers
		self.clock = clk
		self.digital_out = d_out
		self.digital_in = d_in
		self.cs = cs
		self.fsr = 0
		# Set up pins
		GPIO.setup(self.clock, GPIO.OUT)
		GPIO.setup(self.digital_out, GPIO.IN)
		GPIO.setup(self.digital_in, GPIO.OUT)
		GPIO.setup(self.cs, GPIO.OUT)

	# read SPI data from MCP3008 chip, 8 possible adc's (0-7)
	def read_adc(self):
		if self.fsr > 7 or self.fsr < 0:
			return -1
		
		GPIO.output(self.cs, True)
		GPIO.output(self.clock, False)
		GPIO.output(self.cs, False)
		
		commandout = self.fsr
		commandout |= 0x18 # start bit and single-ended bit
		commandout <<= 3 # only need to send 5 bits
		for i in range(5):
			if commandout & 0x80:
				GPIO.output(self.digital_in, True)
			else:
				GPIO.output(self.digital_in, False)
			commandout <<= 1 
			GPIO.output(self.clock, True)
			GPIO.output(self.clock, False)
			
		adcout = 0
		# read in one empty bit, one null bit, and 10 ADC bits
		for i in range(12):
			GPIO.output(self.clock, True)
			GPIO.output(self.clock, False)
			adcout <<= 1
			if GPIO.input(self.digital_out):
				adcout |= 0x1
				
		GPIO.output(self.cs, True)
		adcout >>= 1
		return adcout
	

def fws_read(fws, client):
	while client.alive:
		for f in fws:
			fws_value = f.read_adc()
			if fws_value > 160 and f.status != "open":
				#update what the client sends to differentiate bw free_weights
				client.send('[F]['+f.identifier+']open');
				f.status = "open"
			elif fws_value <= 160 and f.status != "occupied":
				#update what the client sends to differentiate bw free_weights
				client.send('[F]['+f.identifier+']occupied')
				f.status = "occupied"
			print("Value of " + f.identifier + " is : " + str(fws_value) + ". Status of FWS is: " + f.status)
		time.sleep(1)

if __name__ == '__main__':
	client = None
	try:
		fws_a = FreeWeightSensor(18, 23, 24, 25, "a")
		fws_b = FreeWeightSensor(17, 27, 22, 4, "b")
		fws = [fws_a, fws_b]
		client = Client()
		client.send("[F]" + fws[0].station_id)
		fws_thread = threading.Thread(target=fws_read, args=(fws, client,))
		fws_thread.start()
		while True:
			server_msg = client.recv()
			if server_msg == "QUIT":
				print('[WARNING] Closing client because the server closed')
				client.alive = False
				break
		GPIO.cleanup()
	except Exception as e:
		if client:
			client.send("|" + str(fws[0].station_id))
			client.close()
		GPIO.cleanup()
		print(str(e));
		print("except")






















	
