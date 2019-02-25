import bluetooth

serverMacAddress = 'b8:27:eb:b7:2a:37' # need to get server info
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMacAddress, port))
while 1:
	text = raw_input()
	if text == "quit":
		break
	s.send(text)
s.close()
