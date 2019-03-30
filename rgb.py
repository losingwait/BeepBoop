import sys, time
import RPi.GPIO as GPIO

red = 11
green = 12
blue = 13

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(red)

def greenOn():
    blink(green)

def blueOn():
    blink(blue)

def redOff():
    turnOff(red)

def greenOff():
    turnOff(green)

def blueOff():
    turnOff(blue)

def main():
    redOn();
    time.sleep(.2)
    redOff()
    greenOn()
    time.sleep(.2)
    greenOff()
    blueOn()
    time.sleep(.2)
    blueOff()
    GPIO.cleanup()
main()
