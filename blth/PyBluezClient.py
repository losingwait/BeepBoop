import bluetooth
import os

class Client(object):
	def __init__(self):
		self.macAddress = 'b8:27:eb:64:21:32'
		self.port = 3
		os.system("sudo hciconfig hci0 piscan")
		self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.socket.connect((self.macAddress, self.port))
		print("Initialized bluetooth client")
		
	def send(self, rfid_uuid):
		self.socket.send(str(rfid_uuid))
	
	def close(self):
		self.socket.close()
		
	def __del__(self):
		self.socket.close()

#~ serverMacAddress = 'b8:27:eb:64:21:32'
#~ port = 3
#~ os.system("sudo hciconfig hci0 piscan")
#~ s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#~ s.connect((serverMacAddress, port))
#~ while 1:
	#~ text = raw_input()
	#~ if text == "quit":
		#~ break
	#~ s.send(text)
#~ s.close()
