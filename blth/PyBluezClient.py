import bluetooth
import os

class Client(object):
	def __init__(self):
		self.macAddress = 'b8:27:eb:58:80:b2'
		self.port = 5
		self.alive = True
		self.ready_read = True
		os.system("sudo hciconfig hci0 piscan")
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.socket.connect((self.macAddress, self.port))
		print("Initialized bluetooth client")
	
	def recv(self):
		try:
			return self.socket.recv(1024)
		except Exception as e:
			print 'Bluetooth client quitting'
			print 'Exception is', e
			 
	def send(self, rfid_uuid):
		self.socket.send(str(rfid_uuid))
	
	def close(self):
		self.socket.close()
		
	def __del__(self):
		self.socket.close()
