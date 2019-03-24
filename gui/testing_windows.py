
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
sys.path.append('..')
from read import RFIDReader

import requests

class BoxExample(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='Hello World')
		
		self.box = Gtk.Box(spacing=6)
		self.add(self.box)
		
		self.button1 = Gtk.Button(label="Amanda")
		self.button1.connect("clicked", self.on_button1_clicked)
		self.box.pack_start(self.button1, True, True, 0)
		
		self.button2 = Gtk.Button(label="Blake")
		self.button2.connect("clicked", self.on_button2_clicked)
		self.box.pack_start(self.button2, True, True, 0)
		
	def on_button1_clicked(self, widget):
		print('Amanda Bsaibes')
		
	def on_button2_clicked(self, widget):
		print('Blake Nelson')

class GridExample(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='Grid Example')
		
		grid = Gtk.Grid()
		self.add(grid)
		
		button1 = Gtk.Button(label='Button 1')
		button2 = Gtk.Button(label='Button 2')
		button3 = Gtk.Button(label='Button 3')
		button4 = Gtk.Button(label='Button 4')
		button5 = Gtk.Button(label='Button 5')
		button6 = Gtk.Button(label='Button 6')
		
		grid.add(button1)
		grid.attach(button2, 1, 0, 2, 1)
		grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
		grid.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
		grid.attach(button5, 1, 2, 1, 1)
		grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)

class EntryExample(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='Entry Example')
		self.card_reader = RFIDReader()
		self.rfid_value = ''
		self.name = ''
		self.email = ''
		self.password = ''
		self.set_border_width(10)
		self.set_default_size(400,200)
		
		
		grid = Gtk.Grid()
		self.add(grid)
		
		self.entry_name = Gtk.Entry()
		self.entry_name.set_text('')
		self.entry_email = Gtk.Entry()
		self.entry_email.set_text('Enter Email')
		self.entry_password = Gtk.Entry()
		self.entry_password.set_text('Enter Password')
		self.entry_rfid = Gtk.Entry()
		self.entry_rfid.set_text('RFID Value')
		self.entry_rfid.set_editable(False)
		
		self.rfid_button = Gtk.Button(label="Get RFID")
		self.rfid_button.connect('clicked', self.on_rfid_button_clicked)
		
		
		self.submit_button = Gtk.Button(label='Submit')
		self.submit_button.connect("clicked", self.on_submit_button_clicked)
		
		
		grid.attach(self.entry_name, 0, 0, 1, 3)
		grid.attach_next_to(self.entry_email, self.entry_name, Gtk.PositionType.BOTTOM, 1, 3)
		grid.attach_next_to(self.entry_password, self.entry_email, Gtk.PositionType.BOTTOM, 1, 3)
		grid.attach_next_to(self.entry_rfid, self.entry_password, Gtk.PositionType.BOTTOM, 1, 3)
		grid.attach_next_to(self.rfid_button, self.entry_rfid, Gtk.PositionType.BOTTOM, 1, 1)
		
		grid.attach_next_to(self.submit_button, self.rfid_button, Gtk.PositionType.BOTTOM, 1, 1)
		
		
	def on_submit_button_clicked(self, widget):
		print("Sending the information...")
		self.name = self.entry_name.get_text()
		self.email = self.entry_email.get_text()
		self.password = self.entry_password.get_text()
		if self.name == '' or self.email == '' or self.password == '' or self.rfid_value == '':
			print('Need to fill out all fields before submitting a request for a new user')
		else:
			r = requests.post('https://losing-wait.herokuapp.com/users/signup', data = {'name' : name, 'email' : email, 'password' : password, 'rfid' : self.rfid_value})
	
	def on_rfid_button_clicked(self, widget):
		print('Getting RFID value...')
		while(1):
			user_id, user_name = self.card_reader.read()
			if user_id:
				print(user_name, user_id)
				break
		self.entry_rfid.set_text(str(user_id))
		self.rfid_value = str(user_id)
		
class ListBoxExample(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="ListBox Example")
		self.set_border_width(10)
		
		box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(box_outer)
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		box_outer.pack_start(listbox, True, True, 0)
		
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		name = Gtk.Label("Name", xalign=0)
		entry_name = Gtk.Entry()
		entry_name.set_text('')
		
		hbox.pack_start(name, True, True, 0)
		hbox.pack_start(entry_name, True, True, 0)
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		email = Gtk.Label("Email", xalign=0)
		entry_email = Gtk.Entry()
		entry_email.set_text('')
		
		hbox.pack_start(email, True, True, 0)
		hbox.pack_start(entry_email, True, True, 0)
		listbox.add(row)
		
		
		
		
win = ListBoxExample()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()














