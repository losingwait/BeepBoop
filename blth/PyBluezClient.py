import bluetooth
import os

class Client(object):
	def __init__(self):
		self.macAddress = 'b8:27:eb:b7:2a:37'
		self.port = 3
		os.system("sudo hciconfig hci0 piscan")
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.socket.connect((self.macAddress, self.port))
		print("Initialized bluetooth client")
		
	def send(rfid_uuid):
		self.socket.send(rfid_uuid)
		
	def __del__(self):
		self.socket.close()
