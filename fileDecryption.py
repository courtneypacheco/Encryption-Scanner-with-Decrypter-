#!/usr/bin/python
from __future__ import print_function

''''''''''''''''''''''''''''''
'       IMPORT LIBRARIES     '
''''''''''''''''''''''''''''''

#GUI related stuff
import Tkinter as tk
import tkMessageBox as msg
from tkFileDialog import askopenfilename

#Image processing / OS stuff
import os
import sys
import Image

#Cryptography related stuff
from Crypto.Cipher import AES
from Crypto.Hash import MD5

#Exporting related stuff
import pickle

''''''''''''''''''''''''''''''
'     DEFINE GLOBAL VARS     '
''''''''''''''''''''''''''''''
global filename
global selectedFile

''''''''''''''''''''''''''''''
'    DEFINE REGULAR VARS     '
''''''''''''''''''''''''''''''
#Create window
top = tk.Tk()

#String vars
selectedFile = tk.StringVar()
selectedFile.set("")

''''''''''''''''''''''''''''''
'         FUNCTIONS          '
''''''''''''''''''''''''''''''
#Opens up dialog box to select file
def getFileName():
	global filename
	global selectedFile
	filename = askopenfilename(filetypes=[("pickle",".p")])
	selectedFile.set(filename)
	selectFile_button.pack()

#Prepare decryption
def prepareDecrypt():
	
	#Hide previous frame
	selectFile_button.pack_forget()
	main_frame.pack_forget()

	#Now show new frame
	decrypt_frame.pack()
	space3.pack()
	enter_salt.pack()
	salt_textbox.pack()
	space4.pack()
	decrypt_button.pack()
	
#Decrypt
def decrypt():
	
	#Get user input & recreate encryption object
	salt = salt_textbox.get()
	try:
		#Load pickle
		fullfile = selectedFile.get()
		filename = os.path.split(fullfile)[1]
		im_info = pickle.load(open(filename,"rb"))

		#Now hash the entered password
		h = MD5.new()
		h.update(salt)
		key = h.hexdigest()

		#Recreate encryption object
		encrypt_obj = AES.new(key,AES.MODE_CFB,im_info['iv'])

		#Now attempt to decrypt
		decrypted_bytes = encrypt_obj.decrypt(im_info['bytes'])

		#Create image object from decrypted bytes
		mode = im_info['mode']
		dims = tuple(im_info['dims'])
		decrypted_im = Image.fromstring(mode,dims,decrypted_bytes)

		#Show image - the image is saved as a 'tmp' file & deletes itself automatically on Ubuntu once it's closed
		decrypted_im.show()


	except ValueError:
		msg.showwarning("ERROR","Invalid salt.")

''''''''''''''''''''''''''''''
'            MAIN            '
''''''''''''''''''''''''''''''
bgcolor = '#D1E8FF'
buttonColor = '#6DCBE8'
boldText = '#0066CC'

#Set attributes for window
x = 400
y = 300
top.minsize(width=x,height=y)
top.maxsize(width=2*x,height=2*y)

#title
top.wm_title("File Decrypter")

#Frames
main_frame = tk.Frame(width=x,height=y,bg=bgcolor)
decrypt_frame = tk.Frame(width=x,height=x,bg=bgcolor)

#Buttons
openFile_button = tk.Button(main_frame,text="Open File",command=getFileName)
selectFile_button = tk.Button(main_frame,text="Decrypt this file",command=prepareDecrypt)
decrypt_button = tk.Button(decrypt_frame,text="Decrypt",command=decrypt)

#Labels
space = tk.Label(main_frame,text="")
space1 = tk.Label(main_frame,text="")
space2 = tk.Label(main_frame,text="")
space3 = tk.Label(decrypt_frame,text="")
space4 = tk.Label(decrypt_frame,text="")
space5 = tk.Label(decrypt_frame,text="")

file_label1 = tk.Label(main_frame,text="Selected file: ")
file_label2 = tk.Label(main_frame,textvar=selectedFile,font=("Helvetica",11,"bold"),fg=boldText)
enter_salt = tk.Label(decrypt_frame,text="Enter salt:")
file_decrypted = tk.Label(decrypt_frame,text="File decrypted and saved as:")

#Textboxes
salt_textbox = tk.Entry(decrypt_frame,show="*",width=10)

#Set colors
top.config(bg=bgcolor)
space.config(bg=bgcolor)
space1.config(bg=bgcolor)
space2.config(bg=bgcolor)
space3.config(bg=bgcolor)
space4.config(bg=bgcolor)
space5.config(bg=bgcolor)
enter_salt.config(bg=bgcolor)
file_label1.config(bg=bgcolor)
file_label2.config(bg=bgcolor)
file_decrypted.config(bg=bgcolor)

selectFile_button.config(bg=buttonColor)
openFile_button.config(bg=buttonColor)
decrypt_button.config(bg=buttonColor)

#Now pack
main_frame.pack()
space.pack()
openFile_button.pack()
space1.pack()
file_label1.pack()
file_label2.pack()
space2.pack()
