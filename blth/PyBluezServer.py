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
		self.polling_clients = {}
		self.server_alive = True;
		os.system("sudo hciconfig hci0 piscan")
	
	# Poll for status of all machines connected to the hub
	def pollStatus(self):
		print("Starting polling thread")
		while self.server_alive:
			# Collect IDs of stations connected to hub to check status info from DB
			station_ids = []
			for client in self.polling_clients:
				station_ids.append(client.encode())
				
			# Request statuses
			data = {'station_list': station_ids}
			#~ print "Sending: ", data
			response = requests.get('https://losing-wait.herokuapp.com/machines/status', json = {'station_list': station_ids})
			response_dict = self.convertJsonToDict(response.text)
			#~ print "Response from Polling is " + str(response_dict)
			
			# Tell each station its status
			try:
				for station_id in response_dict:
					self.clients[station_id.encode()]["client-sock"].send('P|' + response_dict[station_id.encode()])
					#~ self.clients[station_id.encode()]["client-sock"].send('P|queued')
			except:
				pass
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
					if rfid[0] == '|':
						print("[WARNING] client is quitting")
						self.clients.pop(rfid[1:], None)
						client_sock.close()	
						break
					indicator = rfid[0:3]
					rfid = rfid[3:]
					if indicator == "[R]":
						print "Sent rfid", str(rfid)
						if rfid and self.server_alive:	# AND server_alive in case server dies while waiting for client_sock (TODO: is that needed if its not blocking?)
							print "[Server Received:]", rfid
							print "Sent station id", str(station_id)
							# TODO: change to .json()?
							response = requests.post('https://losing-wait.herokuapp.com/machine_users/checkin', data = {'station_id': station_id, 'rfid' : rfid})
							print(response.text)
							print(response.status_code, type(response.status_code))
							#~ response.status_code = 403
							# User not in queue for the machine
							if response.status_code == 403:
								print("NOT TODAY")
								client_sock.send("R|denied")
							elif response.status_code == 200:
								print("yEET")
								status = self.convertJsonToDict(response.text)
								print status
								if status['checkin'] and not status['checkout']:
									client_sock.send("R|occupied")
								elif not status['checkin'] and status['checkout']:
									if status['status'] == 'queued':
										client_sock.send('R|queued')
									elif status['status'] == 'open':
										client_sock.send("R|open")									
							else:
								# Maybe actually do something in this instance
								# Send to admin?
								print("Shit sux yo")
								client_sock.send("R|error")
					elif indicator == "[F]":
						### Received data from the FSR
						# rfid at this point is [<identifier>]<status>
						rfid = rfid[1:]
						identifier, fws_status = rfid.split(']')
						print "[FSR Message]", identifier, fws_status 	
						if fws_status == 'open':
							response = requests.post('https://losing-wait.herokuapp.com/free_weights/status', data = {'station_id' : station_id+identifier, 'available' : 'true'})
						elif fws_status == 'occupied':
							response = requests.post('https://losing-wait.herokuapp.com/free_weights/status', data = {'station_id' : station_id+identifier, 'available' : 'false'})
						print("Station id is " + str(station_id))
						if response.status_code == 200:
							print("BOI")
							print(response.text)
						else:
							print("An error occurred (& also u suck)") 
							print(response.text)
							
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
			# Create thread to poll for status of current stations
			polling_thread = threading.Thread(target=self.pollStatus)
			polling_thread.start()
			while True:
				# Accept new connection
				client_sock, client_info = self.server_sock.accept() # Blocks
				client_msg = client_sock.recv(self.size).decode()
				
				indicator = client_msg[0:3]
				station_id = client_msg[3:]
				self.clients[station_id] = {"client-sock" : client_sock, "status": "open"}
				if indicator == "[R]":
					self.polling_clients[station_id] = {"client-sock" : client_sock, "status": "open"}
				# Thread for new connection
				client_thread = threading.Thread(target=self.connectionHandler, args=(client_sock, station_id))
				client_thread.start()
				
				

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



