import bluetooth
import os
import json
import time
import threading
import requests

class Hub(object):
	def __init__(self):
		self.host_mac_address = 'b8:27:eb:58:80:b2'
		self.port = 4
		self.backlog = 1
		self.size = 1024
		self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.server_sock.bind((self.host_mac_address, self.port))
		self.server_sock.listen(self.backlog)
		self.clients = {}
		self.server_alive = True;
		os.system("sudo hciconfig hci0 piscan")
	
	def pollStatus(self):
		while True:
			station_ids = []
			for client in self.clients:
				station_ids.append(client.encode())
			data = {'station_list': station_ids}
			print(data)
			response = requests.get('https://losing-wait.herokuapp.com/machines/status', json = {'station_list': station_ids})
			response_dict = self.convertJsonToDict(response.text)
			print "Response from Polling is " + str(response_dict)
			for station_id in response_dict:
					self.clients[station_id.encode()]["client-sock"].send('P|' + response_dict[station_id.encode()])
				
			time.sleep(5)
		
	def convertJsonToDict(self, json_obj):
		json_string = json_obj.replace("'", "\"")
		json_dict = json.loads(json_string)
		return json_dict
	
	def connectionHandler(self, client_sock, station_id):
		print(client_sock)
		client_sock.setblocking(False)
		try:
			while self.server_alive:
				try:
					data = client_sock.recv(self.size)
					if data and self.server_alive:
						print "[Server Received:]", data.decode()
						rfid = data.decode()
						print "Sent station id", str(station_id)
						print "Sent rfid", str(rfid)
						response = requests.post('https://losing-wait.herokuapp.com/machine_users/checkin', data = {'station_id': station_id, 'rfid' : rfid})
						print(response.text)
						if response.status_code is not 200:
							print("Shit sux yo")
						else:
							print("yEET")
							#~ json_string = response.text.replace("'", "\"")
							#~ status = json.loads(json_string)
							status = self.convertJsonToDict(response.text)
							print status
							if status['checkin'] == True and status['checkout'] == False:
								client_sock.send("R|occupied")
							elif status['checkin'] == False and status['checkout'] == True:
								client_sock.send("R|open")
								
				except bluetooth.btcommon.BluetoothError:
					pass
			client_sock.close()
		except:
			print("[WARNING] Client socket closed, ending connection")
			self.clients.pop(client_sock, None)
			client_sock.close()	
		
	def accept_connection(self):
		try:
			while True:
				client_sock, client_info = self.server_sock.accept()
				station_id = client_sock.recv(self.size)
				self.clients[station_id.decode()] = {"client-sock" : client_sock, "status": "open"}
				client_thread = threading.Thread(target=self.connectionHandler, args=(client_sock, station_id.decode()))
				client_thread.start()
				polling_thread = threading.Thread(target=self.pollStatus)
				polling_thread.start()

		except KeyboardInterrupt:
			print("\n[WARNING] Closing Server, sending quit request to all clients")
			for client in self.clients:
				try:
					self.clients[client]["client-sock"].send("QUIT")
				except:
					continue
			print("Sending complete.")
			self.server_alive = False
			self.server_sock.close()

if __name__ == '__main__':
	hub = Hub()
	hub.accept_connection()



