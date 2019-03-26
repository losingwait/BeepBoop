import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
sys.path.append('..')
from RFID_Station_Reader import RFIDReader

import requests

class UserRegistration(Gtk.Window):
	def __init__(self):
		self.card_reader = RFIDReader()
		self.rfid_value = ''
		self.name = ''
		self.email = ''
		self.password = ''
		
		Gtk.Window.__init__(self, title='Entry Example')
		self.set_border_width(10)
		self.set_default_size(400,200)
		header_bar = Gtk.HeaderBar()
		header_bar.set_show_close_button(True)
		header_bar.props.title = 'User Registration'
		self.set_titlebar(header_bar)
		
		box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(box_outer)
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		box_outer.pack_start(listbox, True, True, 0)
		
		### Name ###
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		name = Gtk.Label("Name", xalign=0)
		self.entry_name = Gtk.Entry()
		self.entry_name.set_text('')
		hbox.pack_start(name, True, True, 0)
		hbox.pack_start(self.entry_name, False, True, 0)
		listbox.add(row)
		
		### Email ###
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		email = Gtk.Label("Email", xalign=0)
		self.entry_email = Gtk.Entry()
		self.entry_email.set_text('')
		hbox.pack_start(email, True, True, 0)
		hbox.pack_start(self.entry_email, False, True, 0)
		listbox.add(row)
		
		### Password ###
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		password = Gtk.Label("Password", xalign=0)
		self.entry_password = Gtk.Entry()
		self.entry_password.set_text('')
		hbox.pack_start(password, True, True, 0)
		hbox.pack_start(self.entry_password, False, True, 0)
		listbox.add(row)
		
		### RFID ###
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		rfid = Gtk.Label("RFID", xalign=0)
		self.entry_rfid = Gtk.Entry()
		self.entry_rfid.set_text('RFID Value')
		self.entry_rfid.set_editable(False)
		hbox.pack_start(rfid, True, True, 0)
		hbox.pack_start(self.entry_rfid, False, True, 0)
		listbox.add(row)
		
		### Buttons ###
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		self.rfid_button = Gtk.Button(label="Get RFID")
		self.rfid_button.connect('clicked', self.on_rfid_button_clicked)	
		self.submit_button = Gtk.Button(label='Submit')
		self.submit_button.connect("clicked", self.on_submit_button_clicked)
		hbox.pack_start(self.rfid_button, True, False, 0)
		hbox.pack_start(self.submit_button, True, False, 0)
		listbox.add(row)
		
		#~ self.entry_name = Gtk.Entry()
		#~ self.entry_name.set_text('Enter Name')
		#~ self.entry_email = Gtk.Entry()
		#~ self.entry_email.set_text('Enter Email')
		#~ self.entry_password = Gtk.Entry()
		#~ self.entry_password.set_text('Enter Password')
		#~ self.entry_rfid = Gtk.Entry()
		#~ self.entry_rfid.set_text('RFID Value')
		#~ self.entry_rfid.set_editable(False)

		
		
		#~ grid.add(self.entry_name)
		#~ grid.attach_next_to(self.entry_email, self.entry_name, Gtk.PositionType.BOTTOM, 1, 3)
		#~ grid.attach_next_to(self.entry_password, self.entry_email, Gtk.PositionType.BOTTOM, 1, 3)
		#~ grid.attach_next_to(self.entry_rfid, self.entry_password, Gtk.PositionType.BOTTOM, 1, 3)
		#~ grid.attach_next_to(self.rfid_button, self.entry_rfid, Gtk.PositionType.BOTTOM, 1, 1)
		
		#~ grid.attach_next_to(self.submit_button, self.rfid_button, Gtk.PositionType.BOTTOM, 1, 1)
		
		
	def on_submit_button_clicked(self, widget):
		print("Sending the information...")
		self.name = self.entry_name.get_text()
		self.email = self.entry_email.get_text()
		self.password = self.entry_password.get_text()
		if self.name == '' or self.email == '' or self.password == '' or self.rfid_value == '':
			print('Need to fill out all fields before submitting a request for a new user')
		else:
			r = requests.post('https://losing-wait.herokuapp.com/users/signup', data = {'name' : self.name, 'email' : self.email, 'password' : self.password, 'rfid' : self.rfid_value})
	
	def on_rfid_button_clicked(self, widget):
		print('Getting RFID value...')
		while(1):
			user_id, user_name = self.card_reader.read()
			if user_id:
				print(user_name, user_id)
				break
		self.entry_rfid.set_text(str(user_id))
		self.rfid_value = str(user_id)
		
try:
	win = UserRegistration()
	win.connect('destroy', Gtk.main_quit)
	win.show_all()
	print("before GTK main")
	Gtk.main()
	print("after GTK main")
except:
	print("Here")
	win.close()














