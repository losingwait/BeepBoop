import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
sys.path.append('..')
from RFID_Station_Reader import RFIDReader

import requests

class UpdateUserDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "[WARNING] Update User ID", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_border_width(10)
		self.set_default_size(300, 200)
		header_bar = Gtk.HeaderBar()
		header_bar.set_show_close_button(True)
		header_bar.props.title = 'Update User ID'
		self.set_titlebar(header_bar)
		label = Gtk.Label("Are you sure you want to update " + parent.name + "'s ID?")
		box = self.get_content_area()
		box.add(label)
		self.show_all()
		
class IncompleteInformationDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Incomplete Information", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_border_width(10)
		self.set_default_size(100, 200)
		header_bar = Gtk.HeaderBar()
		header_bar.set_show_close_button(True)
		header_bar.props.title = 'Incomplete Information'
		self.set_titlebar(header_bar)
		label = Gtk.Label("All the information must be filled out")
		box = self.get_content_area()
		box.add(label)
		self.show_all()

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
		self.entry_password.set_visibility(False)
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
		
		
	def on_submit_button_clicked(self, widget):
		self.name = self.entry_name.get_text()
		self.email = self.entry_email.get_text()
		self.password = self.entry_password.get_text()
		#or self.rfid_value == ''
		if self.name == '' or self.email == '' or self.password == '':
			incomplete_dialog = IncompleteInformationDialog(self)
			incomplete_response = incomplete_dialog.run()
			if incomplete_response == Gtk.ResponseType.OK:
				incomplete_dialog.destroy()
			return
		else:
			#check if the user exists in the database
			response = requests.post('', data = {})
			if response.status_code is 200:
				#user exists in the database
				#check user password -- if correct
				
				update_user_dialog = UpdateUserDialog(self)
				update_user_response = update_user_dialog.run()
				
				if update_user_response == Gtk.ResponseType.OK:
					print("OK button clicked")
					r = requests.post('https://losing-wait.herokuapp.com/users/signup', data = {'name' : self.name, 'email' : self.email, 'password' : self.password, 'rfid' : self.rfid_value})
					update_user_dialog.destroy()
				elif update_user_response == Gtk.ResponseType.CANCEL:
					print("Cancel Button clicked")
					update_user_dialog.destroy()
					return

			else:
				r = requests.post('https://losing-wait.herokuapp.com/users/signup', data = {'name' : self.name, 'email' : self.email, 'password' : self.password, 'rfid' : self.rfid_value})

		#~ if self.name == '' or self.email == '' or self.password == '' or self.rfid_value == '':
			#~ print('Need to fill out all fields before submitting a request for a new user')
		#~ else:
			#~ 
	
	def on_rfid_button_clicked(self, widget):
		print('Getting RFID value...')
		while(1):
			user_id = self.card_reader.read()
			if user_id:
				print(user_id)
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














