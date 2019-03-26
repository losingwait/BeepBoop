import bluetooth
import os
import threading
import requests

def connectionHandler(client_sock):
	size = 1024
	print(client_sock)
	client_sock.setblocking(False)
	try:
		while server_alive:
			try:
				data = client_sock.recv(size)
				if data and server_alive:
					print "[Server Received:]", data.decode()
					#~ response = requests.post("")
					
			except bluetooth.btcommon.BluetoothError:
				pass
		client_sock.close()
	except:
		print("[WARNING] Client socket closed, ending connection")
		client_socks.remove(client_sock)
		client_sock.close()


host_mac_address = 'b8:27:eb:58:80:b2'
port = 4
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

except KeyboardInterrupt:
	print("[WARNING] Closing Server, sending quit request to all clients")
	for sock in client_socks:
		try:
			sock.send("QUIT")
		except:
			continue
	print("Sending complete.")
	server_alive = False
	s.close()
