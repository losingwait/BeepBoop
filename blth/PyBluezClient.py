import bluetooth
import os

class Client(object):
	def __init__(self):
		self.macAddress = 'b8:27:eb:58:80:b2'
		self.port = 4
		self.alive = True
		os.system("sudo hciconfig hci0 piscan")
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.socket.connect((self.macAddress, self.port))
		print("Initialized bluetooth client")
	
	def recv(self):
		return self.socket.recv(1024)
			
	def send(self, rfid_uuid):
		self.socket.send(str(rfid_uuid))
	
	def close(self):
		self.socket.close()
		
	def __del__(self):
		self.socket.close()
