import bluetooth
import os

hostMacAddress = 'b8:27:eb:b7:2a:37'
port = 3
backlog = 1
size = 1024
os.system("sudo hciconfig hci0 piscan")
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMacAddress, port))
s.listen(backlog)
try:
	client, clientInfo = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data)
except:
	print("closing socket")
	client.close()
	s.close()
