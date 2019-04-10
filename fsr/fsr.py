import time
import os
import RPi.GPIO as GPIO
import netifaces
import requests

class FreeWeightSensor(object):
	def __init__(self):
		self.status = "open"
		self.station_id = str(netifaces.ifaddresses('wlan0')[netifaces.AF_LINK][0]['addr'])
		GPIO.setmode(GPIO.BCM)
		DEBUG = 1
		# Port Numbers
		self.clock = 18
		self.digital_out = 23
		self.digital_in = 24
		self.cs = 25
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
	

if __name__ == '__main__':
	try:
		free_weight_sensor = FreeWeightSensor()
		while True:
			fws_value = free_weight_sensor.read_adc()
			
			if fws_value > 160 and free_weight_sensor.status != "open":
				# free weight is on the stand but the status is not updated
				# api call to database to free the status
				reply = requests.post('https://losing-wait.herokuapp.com/free_weights/status', data = {'stations_id' : free_weight_sensor.station_id, 'available' : 'true'})
				if reply.status_code == 200:
					free_weight_sensor.status = "open"
					print("Changing status to OPEN. Value is: " + str(fws_value))
				else:
					print("shit sucks")
			elif fws_value <= 160 and free_weight_sensor.status != "occupied":
				# free weight is not on the stand but the status is not updated
				# api call to database to occupy the status
				reply = requests.post('https://losing-wait.herokuapp.com/free_weights/status', data = {'stations_id' : free_weight_sensor.station_id, 'available' : 'false'})
				if reply.status_code == 200:
					free_weight_sensor.status = "occupied"
					print("Changing status to OCCUPIED. Value is: " + str(fws_value))
				else:
					print("shit sucks")
			else:
				print("Value is: " + str(fws_value) + ". Status of FWS is: " + free_weight_sensor.status)
			time.sleep(1)
	except Exception as e:
		GPIO.cleanup()
		print(str(e));
		print("except")






















	
