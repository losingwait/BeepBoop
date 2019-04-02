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
	
	# Poll for status of all machines connected to the hub
	def pollStatus(self):
		print("Starting polling thread")
		while True:
			# Collect IDs of stations connected to hub to check status info from DB
			station_ids = []
			for client in self.clients:
				station_ids.append(client.encode())
				
			# Request statuses
			data = {'station_list': station_ids}
			#~ print "Sending: ", data
			response = requests.get('https://losing-wait.herokuapp.com/machines/status', json = {'station_list': station_ids})
			response_dict = self.convertJsonToDict(response.text)
			#~ print "Response from Polling is " + str(response_dict)
			
			# Tell each station its status
			for station_id in response_dict:
				self.clients[station_id.encode()]["client-sock"].send('P|' + response_dict[station_id.encode()])
				
			time.sleep(5)
		
	def convertJsonToDict(self, json_obj):
		json_string = json_obj.replace("'", "\"")
		json_dict = json.loads(json_string)
		return json_dict
	
	# What to do when a bluetooth connection is made between a station and a hub
	def connectionHandler(self, client_sock, station_id):
		print "Starting connection handler for",
		print(client_sock)
		# TODO: if this happens indiscriminately, should it be done when connection is made?
		client_sock.setblocking(False)
		try:
			while self.server_alive:
				try:
					rfid = client_sock.recv(self.size).decode()
					print "Sent rfid", str(rfid)
					if rfid and self.server_alive:	# AND server_alive in case server dies while waiting for client_sock (TODO: is that needed if its not blocking?)
						print "[Server Received:]", rfid
						print "Sent station id", str(station_id)
						# TODO: change to .json()?
						response = requests.post('https://losing-wait.herokuapp.com/machine_users/checkin', data = {'station_id': station_id, 'rfid' : rfid})
						print(response.text)
						if response.status_code is not 200:
							print("Shit sux yo")
						else:
							print("yEET")
							status = self.convertJsonToDict(response.text)
							print status
							if status['checkin'] and not status['checkout']:
								client_sock.send("R|occupied")
							elif not status['checkin'] and status['checkout']:
								client_sock.send("R|open")
					else:
						print("No data or server is not alive")
								
				except bluetooth.btcommon.BluetoothError:
					continue
			client_sock.close()
		except Exception as e:
			print("[WARNING] Client socket closed, ending connection ({})".format(type(e)))
			self.clients.pop(client_sock, None)
			client_sock.close()	

	# Continuously accept bluetooth connections
	def accept_connection(self):
		try:
			while True:
				# Accept new connection
				client_sock, client_info = self.server_sock.accept() # Blocks
				station_id = client_sock.recv(self.size).decode()
				self.clients[station_id] = {"client-sock" : client_sock, "status": "open"}
				
				# Thread for new connection
				client_thread = threading.Thread(target=self.connectionHandler, args=(client_sock, station_id))
				client_thread.start()
				
				# Create thread to poll for status of current stations
				# TODO: Do we need a new thread every time a new connection is made? Should this be before the while loop?
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
			
		except Exception as e:
			print("[FATAL] Error occured while accepting connections: " + str(e))

if __name__ == '__main__':
	hub = Hub()
	hub.accept_connection()



