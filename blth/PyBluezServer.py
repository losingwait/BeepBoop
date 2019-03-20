import bluetooth
import os
import threading

def connectionHandler(client_sock):
	size = 1024
	print(client_sock)
	try:
		while server_alive:
			data = client_sock.recv(size)
			print("after sock recv")
			if data and server_alive:
				print(data.decode())
		print("after while loop")
		client_sock.close()
	except:
		print("[WARNING] Client socket closed, ending connection")
		client_socks.remove(client_sock)
		client_sock.close()


host_mac_address = 'b8:27:eb:64:21:32'
port = 3
backlog = 1
size = 1024
os.system("sudo hciconfig hci0 piscan")
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((host_mac_address, port))
s.listen(backlog)
client_socks = []
server_alive = True

try:
	while 1:
		client_sock, client_info = s.accept()
		client_socks.append(client_sock)
		client_thread = threading.Thread(target=connectionHandler, args=(client_sock, ))
		client_thread.start()
	
except:
	print("[WARNING] Closing Server, sending quit request to all clients")
	server_alive = False
	s.close()
