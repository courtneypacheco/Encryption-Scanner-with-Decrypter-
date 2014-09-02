#!/usr/bin/python
from __future__ import print_function

''''''''''''''''''''''''''''''
'       IMPORT LIBRARIES     '
''''''''''''''''''''''''''''''

#GUI related stuff
import Tkinter as tk
import tkMessageBox as msg

#Scanner related stuff
import sys
import sane
import Image

#Cryptography related stuff
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import MD5

#Exporting related stuff
import re
import pickle

''''''''''''''''''''''''''''''
'   ESTABLISH GLOBAL VARS    '
''''''''''''''''''''''''''''''
global s
global im_bytes
global salt
global encrypt_obj
global encrypted_bytes
global im
global iv

#Find PIL modules
sys.path.append('../PIL')


''''''''''''''''''''''''''''''
'         FUNCTIONS          '
''''''''''''''''''''''''''''''

#Get list of devices from SANE
def getDevices():

	#Initialize SANE
	sane.init()

	#Get list of devices & let user know the list of devices has been selected
	devices = sane.get_devices()
	scanners_found.pack()

	#Insert options into the listbox. Certain Linux distributions sometimes have issues with
	#obtaining a list of devices from SANE, so users may need to press "Find Scanners" twice.
	#(When "Find Scanners" is pressed the first time, sometimes the list of devices returned is
	#empty.) The purpose of this "if" statement is to check if the device list is empty or not.	
	if (len(devices) != 0):
		count = 1
		for device in devices:
			device_name = device[1] + " " + device[2]
			devices_listbox.insert(count,device_name)
			count += 1
	

		#Disable "Get Devices" button
		getDevices_button.config(state='disabled')

		#Now display a button to let the user select the scanner
		Select_button.pack()
		scanners_found.pack_forget()
	else:
		Select_button.pack_forget()
		scanners_found.pack()
		
	
def selectDevice():
	#Unpack previous frame & reset to initial conditions
	scanners_found.pack_forget()
	main_frame.pack_forget()

	#Now pack next frame
	scan_frame.pack()
	spaceextra.pack()
	make_scan_button.pack()

#Press this button to make a scan
def scanNow():
	global s
	global im_bytes
	global salt
	global im

	#Let user know that scanning has begun.
	space2.pack()
	scanning_now.pack()
	make_scan_button.config(state="disabled")

	#Get selected device *index*
	selected_device = devices_listbox.index("active")

	#Scan
	try:
		s = sane.open(sane.get_devices()[selected_device][0])
		#s.mode = 'color'
		s.br_x=320. ; s.br_y=240.

		#Start scan
		s.start()

		#Give user option to cancel scan if the scan gets stuck
		cancelScan_button.pack()

		#Get an image object -- but do not show a preview. (Showing a preview saves
		#the scanned image to a file in the tmp directory, which we don't want.)
		im=s.snap()

		#Convert image to bytes
		im_bytes = im.tobytes()

		#Remove buttons that are no longer necessary
		make_scan_button.pack_forget()
		cancelScan_button.pack_forget()
		scanning_now.pack_forget()
		scan_frame.pack_forget()

		#Send message that says scan is complete.
		scan_complete.pack()

		#add spacer
		space3.pack()

		#Ask user to enter salt
		salt_frame.pack()
		space4.pack()
		enter_salt.pack()
		salt1.pack()
		salt_textbox.pack()
		salt2.pack()
		retype_salt_textbox.pack()
		space5.pack()

		#Add encrypt button now
		encrypt_button.pack()

	except: 
		make_scan_button.config(state="normal")
		msg.showwarning("SCANNER CONNECTION LOST","Connection to your scanner has been lost. Make sure your scanner is not in 'sleep mode' and that your scanner is plugged in. For security purposes, please restart this program.")

#Cancels scan
def cancelScan():
	global s
	s.cancel()
	cancelScan_button.pack_forget()
	scanning_now.pack_forget()
	make_scan_button.config(state="normal")

#encrypt the image
def encrypt():
	global salt
	global encrypt_obj
	global im_bytes
	global encrypted_bytes
	global iv

	#Create initialization vector
	iv = Random.new().read(AES.block_size)

	#Get user typed salts
	salt = salt_textbox.get()
	retyped_salt = retype_salt_textbox.get()

	#Now check if both salt fields are equal (Want to make sure the user typed their salt correctly)
	if (salt == retyped_salt):

		#Now hash the password
		h = MD5.new()
		h.update(salt)
		key = h.hexdigest()

		#Create encryption object and encrypt
		encrypt_obj = AES.new(key,AES.MODE_CFB,iv)
		encrypted_bytes = encrypt_obj.encrypt(im_bytes)

		#Now remove the old frame and add the new frame
		salt_frame.pack_forget()
		encrypt_frame.pack()
		space6.pack()
		encryption_complete.pack()
		filename_textbox.pack()
		space7.pack()
		saveSend_button.pack()
			
			
	else:
		msg.showwarning("ERROR","Your salts do not match. Please recheck what you've typed.")
	
#Save file
def save():
	global encrypted_bytes
	global im
	fname = filename_textbox.get()
	
	#Check if filename is alphanumeric
	is_alphanumeric = re.match('^[\w=]+$',fname) is not None

	if (is_alphanumeric == True):

		#Store relevant info in a dictionary object
		data = dict()
		data['mode'] = im.mode
		data['dims'] = im.getbbox()[2:]
		data['iv'] = iv
		data['bytes'] = encrypted_bytes

		#Save file
		pickle_name = fname + ".p"
		pickle.dump(data,open(pickle_name,"wb"))

		#Now leave message:
		encrypt_frame.pack_forget()
		sent_frame.pack()
		space8.pack()
		file_sent.pack()
	else:
		msg.showwarning("INVALID FILENAME","Your filename can only contain alphanumeric characters and dashes.")

#Display version history
def versionHistory():
	msg.showinfo("Version History","Version 1.0.0 \n\nCreated by Courtney Pacheco on Aug 13, 2014 \n\nLast updated: Never")
	

#Display program use
def programUse():
	msg.showinfo("Program Use","This program allows you to scan documents from any scanner/printer connected to your computer and encrypts the BYTES of your scanned documents. Encrypted bytes are then saved to a Python 'Pickle' file, and at this point, you can send the file to an encrypted server for added security. Those bytes can be decrypted with the proper program to reveal the original image.")

#Help info
def helpScanner():
	msg.showinfo("Can't Find Scanner","If this program cannot find your scanner, try resetting your scanner connection by unplugging your scanner and plugging it back in. Make sure the scanner is on and ready to scan. Sometimes the scanner falls asleep, resulting in a lost connection.")

def helpExtension():
	msg.showinfo("Why are my files saved as '.p' files?","The .p extension represents a Python Pickle file. Python Pickle files are simply Python objects, and can only be opened with Python.")


''''''''''''''''''''''''''''''
'            MAIN            '
''''''''''''''''''''''''''''''
bgcolor = '#D1E8FF'
buttonColor = '#6DCBE8'
boldText = '#0066CC'

#Create window
top = tk.Tk()
x = 400
y = 300
top.minsize(width=x,height=y)
top.maxsize(width=2*x,height=2*y)

#title
top.wm_title("Encryption Scanner")

#Frames
main_frame = tk.Frame(width=x,height=y,bg=bgcolor)
scan_frame = tk.Frame(width=3*x/4,height=3*y/4,bg=bgcolor)
back_frame = tk.Frame(width=x/4,height=y/4,bg=bgcolor)
salt_frame = tk.Frame(width=x,height=y,bg=bgcolor)
encrypt_frame = tk.Frame(width=x,height=y,bg=bgcolor)
sent_frame = tk.Frame(width=x,height=y,bg=bgcolor)

#Spacers
space = tk.Label(main_frame, text = "")
space1 = tk.Label(main_frame, text = "")
space2 = tk.Label(scan_frame, text = "")
space3 = tk.Label(salt_frame, text = "")
space4 = tk.Label(salt_frame, text = "")
space5 = tk.Label(salt_frame, text = "")
space6 = tk.Label(encrypt_frame, text = "")
space7 = tk.Label(encrypt_frame, text = "")
space8 = tk.Label(sent_frame, text = "")
spaceextra = tk.Label(scan_frame, text="")
spaceextra2 = tk.Label(main_frame, text="")

#Create a listbox to store the scanner names
devices_listbox = tk.Listbox(main_frame)
devices_listbox.config(height=5)

#Buttons
getDevices_button = tk.Button(main_frame, text="Find Scanners", command=getDevices, highlightthickness=0)
Select_button = tk.Button(main_frame, text="Select Scanner", bg="yellow", command=selectDevice, highlightthickness=0)
make_scan_button = tk.Button(scan_frame, text="Scan Now",command=scanNow, highlightthickness=0)
cancelScan_button = tk.Button(scan_frame, text="CANCEL SCAN",command=cancelScan,bg="red", highlightthickness=0)
encrypt_button = tk.Button(salt_frame, text="Encrypt File", command=encrypt, highlightthickness=0)
saveSend_button = tk.Button(encrypt_frame, text="Save",command=save, highlightthickness=0)


#Status messages
scanners_found = tk.Label(main_frame,text="No scanners found. Try again.",font=("Helvetica",10,"bold"),fg=boldText)
selected_scanner = tk.Label(scan_frame, text="Selected Scanner:")
scanning_now = tk.Label(scan_frame,text="Scanning now... Please wait.")
scan_complete = tk.Label(salt_frame,text="Scan complete.",font=("Helvetica",16,"bold"),fg=boldText)
encryption_complete = tk.Label(encrypt_frame,text="Encryption complete. Please enter a name for your file.")
file_sent = tk.Label(sent_frame,text="File saved on your local disk.",font=("Helvetica",16,"bold"),fg=boldText)

#Labels
enter_salt = tk.Label(salt_frame,text="Please choose a salt.",font="bold")
salt1 = tk.Label(salt_frame,text='Type salt:')
salt2 = tk.Label(salt_frame,text='Retype salt:')

#Textboxes
salt_textbox = tk.Entry(salt_frame,show="*",width=10)
retype_salt_textbox = tk.Entry(salt_frame,show="*",width=10)
filename_textbox = tk.Entry(encrypt_frame,width=35)

#Pack buttons, etc.
main_frame.pack()
space.pack()
getDevices_button.pack()
spaceextra2.pack()
devices_listbox.pack()
space1.pack()


''''''''''''''''''''''''''''''
'         FILE MENU          '
''''''''''''''''''''''''''''''
menubar = tk.Menu(top)

#about menu
about = tk.Menu(menubar)
about.add_command(label="Program use", command=programUse)
about.add_command(label="Version History", command=versionHistory)
menubar.add_cascade(label="About",menu=about)

#help menu
help = tk.Menu(menubar)
help.add_command(label="This program is not finding my scanner", command=helpScanner)
help.add_command(label="Why are my scanned documents saved with the extension .p?", command=helpExtension)
menubar.add_cascade(label="Help",menu=help)
top.config(menu=menubar)

#Set colors
top.config(bg=bgcolor)
space.config(bg=bgcolor)
space1.config(bg=bgcolor)
space2.config(bg=bgcolor)
space3.config(bg=bgcolor)
space4.config(bg=bgcolor)
space5.config(bg=bgcolor)
space6.config(bg=bgcolor)
space7.config(bg=bgcolor)
space8.config(bg=bgcolor)
spaceextra.config(bg=bgcolor)
spaceextra2.config(bg=bgcolor)
scanners_found.config(bg=bgcolor)
scanning_now.config(bg=bgcolor)
scan_complete.config(bg=bgcolor)
enter_salt.config(bg=bgcolor)
encryption_complete.config(bg=bgcolor)
salt1.config(bg=bgcolor)
salt2.config(bg=bgcolor)
file_sent.config(bg=bgcolor)

Select_button.config(bg=buttonColor,borderwidth=2)
getDevices_button.config(bg=buttonColor,borderwidth=2)
make_scan_button.config(bg=buttonColor,borderwidth=2)
encrypt_button.config(bg=buttonColor,borderwidth=2)
saveSend_button.config(bg=buttonColor,borderwidth=2)

top.mainloop()