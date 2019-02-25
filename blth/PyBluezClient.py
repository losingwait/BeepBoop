import bluetooth

class Client(object):
	def __init__(self):
		self.macAddress = 'b8:27:eb:b7:2a:37'
		self.port = 3
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.socket.connect((self.macAddress, self.port))
		
	def send(rfid_uuid):
		self.socket.send(rfid_uuid)
		
	def __del__(self):
		self.socket.close()
