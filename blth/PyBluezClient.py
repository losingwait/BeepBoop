import bluetooth
import os

class Client(object):
	def __init__(self):
		self.macAddress = 'b8:27:eb:58:80:b2'
		self.port = 4
		self.alive = True
		self.ready_read = True
		os.system("sudo hciconfig hci0 piscan")
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		connection_exists = False
		connection_tries = 0
		while not connection_exists and connection_tries < 10:
			try: 
				connection_tries += 1
				self.socket.connect((self.macAddress, self.port))
				connection_exists = True
			except:
				connection_exists = False
		print("Initialized bluetooth client")
	
	def recv(self):
		try:
			response = self.socket.recv(1024)
			return response
		except Exception as e:
			
			print 'Bluetooth client quitting'
			print 'Exception is', e
			 
	def send(self, rfid_uuid):
		self.socket.send(str(rfid_uuid))
	
	def close(self):
		self.socket.close()
		
	def __del__(self):
		self.socket.close()
