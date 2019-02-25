import socket

serverMacAddress = 'b8:27:eb:b7:2a:37' # need to get server info
port = 9
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMacAddress,port))
while 1:
	text = input()
	if text == "quit":
		break
	s.send(bytes(text, 'UTF-8'))
s.close()
