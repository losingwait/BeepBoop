import requests

# Check-in to the gym
r = requests.post('https://losing-wait.herokuapp.com/gym_users/checkin', data = {'rfid' : '123'})

# Check-in to a machine
r = requests.post('https://losing-wait.herokuapp.com/machine_users/checkin', data = {'station_id' : '0', 'rfid' : '123'})

