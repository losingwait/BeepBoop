import bluetooth
import os
import threading

def connectionHandler(client_sock):
	size = 1024
	print(client_sock)
	while 1:
		data = client_sock.recv(size)
		if data:
			print(data.decode())
			client_sock.send(data)


host_mac_address = 'b8:27:eb:64:21:32'
port = 3
backlog = 1
size = 1024
os.system("sudo hciconfig hci0 piscan")
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((host_mac_address, port))
s.listen(backlog)
try:
	client_sock, client_info = s.accept()
	client_thread = threading.Thread(target=connectionHandler, args=(client_sock,))
	client_thread.start()

	
except:
	print("closing socket")
	client.close()
	s.close()
