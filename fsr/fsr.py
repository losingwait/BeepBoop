import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0-7)
def read_adc(adcnum, clockpin, mosipin, misopin, cspin):
	if adcnum > 7 or adcnum < 0:
		return -1
	
	GPIO.output(cspin, True)
	GPIO.output(clockpin, False)
	GPIO.output(cspin, False)
	
	commandout = adcnum
	commandout |= 0x18 # start bit and single-ended bit
	commandout <<= 3 # only need to send 5 bits
	for i in range(5):
		if commandout & 0x80:
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		commandout <<= 1 
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		
	adcout = 0
	# read in one empty bit, one null bit, and 10 ADC bits
	for i in range(12):
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		adcout <<= 1
		if GPIO.input(misopin):
			adcout |= 0x1
	GPIO.output(cspin, True)
	adcout >>= 1
	return adcout
	
# Port Numbers
CLK = 18
DIGITAL_OUT = 23
DIGITAL_IN = 24
CS = 25

FSR = 0

# Set up pins
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIGITAL_OUT, GPIO.IN)
GPIO.setup(DIGITAL_IN, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

while True:
	value = read_adc(FSR, CLK, DIGITAL_IN, DIGITAL_OUT, CS)
	print "Value from FSR is: " + str(value)
	if value > 160:
		print "Free Weight is AVAILABLE"
	else:
		print "Free Weight is TAKEN"
	time.sleep(0.5)





















	
