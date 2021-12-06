#
#ECE480 Design Team 4
#Main UI Code for mmWave data collection project
#
#This code handles the inputs from a rotary encoder and displays the menu on a 20x4 character LCD
#Menu selections call functions from the Beagle_Bone_API file in order to perform sensor functions
#
import logging
import gpio as GPIO
import time
import os
import Beagle_Bone_API

from RPLCD.i2c import CharLCD

def gpio_setup():

	#GPIO Config
	GPIO.setup(pin_rot_a, GPIO.IN)
	GPIO.setup(pin_rot_b, GPIO.IN)
	GPIO.setup(pin_rot_btn, GPIO.IN)

#sets everything needed for the LCD
def lcd_setup():
	#Bitmaps for custom characters
	up_arrow = (
		0b00100,
		0b01110,
		0b11111,
		0b00000,
		0b00000,
		0b00000,
		0b00000,
		0b00000
	)
	down_arrow = (
		0b00000,
		0b00000,
		0b00000,
		0b00000,
		0b00000,
		0b11111,
		0b01110,
		0b00100
	)

	#LCD setup
	global lcd
	lcd = CharLCD(i2c_expander='PCF8574',address=0x27,port=3,cols=20,rows=4)
	lcd.clear()
	lcd.cursor_pos = (0,0)
	
	#create custom characters from bitmap above
	lcd.create_char(0,up_arrow)
	lcd.create_char(1,down_arrow)

#This function is called every time the rotary encoder button is pressed
#It will check the text of the current selection and call the appropiate function
def ui_select():
	selection = current_menu[sel]
	global ui_state
	global json_file_path
	#global uartCom
	print("You Selected: " + selection)
	if (selection == "BACK"):
		draw_main_menu()
		return
	if (selection == "JSON Select"):
		draw_json_menu()
		return
	if (selection == "Chirp Select"):
		draw_chirp_menu()
		return
	if (selection == "Storage"):
		draw_storage_menu()
		return
	if (selection == "Select Storage"):
		return
	if (selection == "Start Recording"):
		#Check to make sure files are set up correctly
		if (json_file_path == "NONE"):
			message("ERROR:\n\rNo JSON selected",3)
			return
		Beagle_Bone_API.radar_record_start(json_file_path)
		return
	if (selection == "Stop Recording"):
		draw_stop_menu()
		return
	if (selection == "Start Sensor"):
		uartCom = Beagle_Bone_API.connect_com_ports("/dev/ttyACM0", "/dev/ttyACM1")
		Beagle_Bone_API.send_sensor_start(uartCom)
		return
	if (selection == "Stop Sensor"):
		uartCom = Beagle_Bone_API.connect_com_ports("/dev/ttyACM0", "/dev/ttyACM1")
		Beagle_Bone_API.send_sensor_stop(uartCom)
		return
	if (ui_state == "stop" and selection == "Stop"):
		Beagle_Bone_API.stop_record(json_file_path)
	if (selection == "Shutdown"):
		draw_shutdown_menu()
		return
	if (ui_state == "shutdown" and selection == "Shutdown"):
		print("OS Shutdown code goes here!")
		return
	if (selection == "Board Reset"):
		draw_reset_menu()
		return
	if (ui_state == "reset" and selection == "Reset"):
		print("board reset code goes here!")
		return
	if (ui_state == "json"):
		json_file_path = sd_base + json_dir + "/" +  selection
		message("JSON File set:\n\r" + json_file_path,3)
		return
	if (ui_state == "chirp"):
		message("Sending chirp file\n\n\rPlease Wait...",0)

		print("Connecting to COM ports ...")
		time.sleep(1.0)
		uartCom = Beagle_Bone_API.connect_com_ports("/dev/ttyACM0", "/dev/ttyACM1")
		chirp_file_path = sd_base + chirp_dir + "/" +  selection

		config_contents = Beagle_Bone_API.get_cfg(chirp_file_path)
		print(chirp_file_path)
		print("Sending chirp file to board...")
		time.sleep(1.0)
		Beagle_Bone_API.send_cfg(config_contents, uartCom)

		update_menu()
		draw_cursor()
		return
#This function is called every time the rotary encoder rotates clockwise. It advances the menu selection
def ui_up():
	global sel
	global frame_shift
	frame_shift_old = frame_shift
	if (sel > 0):
		sel -= 1
	if (sel < frame_shift):
		if (sel == 0):
			frame_shift = 0
		else:
			frame_shift = sel
	#redraw menu if the frame shifts
	if (frame_shift_old != frame_shift):
		update_menu()
	
	draw_cursor()

#This function is called every time the rotary encoder rotates counterclockwise. It advances the menu selection	
def ui_down():
	global sel
	global frame_shift
	frame_shift_old = frame_shift
	if (sel < max_sel - 1):
		sel += 1
	if (sel > frame_shift + 3):
		if (sel < 3):
			frame_shift = 0
		else:
			frame_shift = sel - 3
	#redraw menu if the frame shifts
	print("sel = " + str(sel))
	print("frame_shift = " + str(frame_shift))
	if (frame_shift_old != frame_shift):
		update_menu()
	draw_cursor()
#
#Below are the functions to draw various menus. They are called upon selecting that menu item by the select function
#
def draw_main_menu():
	global ui_state
	ui_state = "menu"
	main_menu = ["Start Recording","Stop Recording","Start Sensor","Stop Sensor", "JSON Select", "Chirp Select", "Storage", "Shutdown", "Board Reset"]
	create_menu(main_menu)
def draw_json_menu():
	global ui_state
	global sd_base
	global json_dir
	ui_state = "json"
	json_menu = ["BACK"]
	#Get list of json files from SD Card
	files = os.listdir(sd_base + json_dir)
	json_menu = json_menu + files
	create_menu(json_menu)
def draw_chirp_menu():
	global ui_state
	global sd_base
	global chirp_dir
	ui_state = "chirp"
	chirp_menu = ["BACK"]
	#Get list of json files from SD Card
	files = os.listdir(sd_base + chirp_dir)
	chirp_menu = chirp_menu + files
	create_menu(chirp_menu)
def draw_storage_menu():
	global ui_state
	ui_state = "storage"
	storage_menu = ["BACK","Select Storage"]
	create_menu(storage_menu)
	st = os.statvfs(sd_base)
	total = (st.f_blocks * st.f_frsize)/(1024 ** 3)
	used = ((st.f_blocks - st.f_bfree) * st.f_frsize)/(1024 ** 3)
	lcd.cursor_pos = (3,1)
	lcd.write_string("Used: " + str(used) + "/" + str(total) + " GiB")
	lcd.cursor_pos = (0,0)
def draw_shutdown_menu():
	global ui_state
	ui_state = "shutdown"
	shutdown_menu = ["BACK", "Shutdown"]
	create_menu(shutdown_menu)
	lcd.cursor_pos = (2,0)
	lcd.write_string("Do you really want\r\nto shut down?")
	lcd.cursor_pos = (0,0)
def draw_reset_menu():
	global ui_state
	ui_state = "reset"
	reset_menu = ["BACK", "Reset"]
	create_menu(reset_menu)
	lcd.cursor_pos = (2,0)
	lcd.write_string("Do you really want\r\nto reset?")
	lcd.cursor_pos = (0,0)
def draw_stop_menu():
	global ui_state
	ui_state = "stop"
	reset_menu = ["BACK", "Stop"]
	create_menu(reset_menu)
	lcd.cursor_pos = (2,0)
	lcd.write_string("Do you really want\r\nto stop recording?")
	lcd.cursor_pos = (0,0)
def draw_dummy_menu():
	dummy_menu = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
	create_menu(dummy_menu)

#This function creates a new menu. It takes a list of menu items and calls the draw_menu function. It automatically resets the cursor and selection.
def create_menu(menu):
	global sel
	global frame_shift
	frame_shift = 0
	sel = 0

	draw_menu(menu)

	#Reset cursor
	lcd.cursor_pos = (0,0)
	lcd.write_string("*")
	lcd.cursor_pos = (0,0)

#Draws a menu. It takes a list of menu items and writes them to the LCD
def draw_menu(menu):
	global current_menu
	global max_sel
	current_menu = menu
	#update variables for selection bounds
	max_sel = len(menu)
	row = 0	
	orig_pos = lcd.cursor_pos
	lcd.clear()
	for i in range(frame_shift,4 + frame_shift):
		lcd.cursor_pos = (row,1)
		if (i < max_sel):
			item = menu[i]
			lcd.write_string(item[0:19])
		row += 1
	if (frame_shift != 0):
		lcd.cursor_pos = (0,19)
		lcd.write_string("\x00")
	if (frame_shift != (max_sel - 4) and max_sel > 4):
		lcd.cursor_pos = (3,19)
		lcd.write_string("\x01")
	lcd.cursor_pos = orig_pos

#This updates the menu when the frame shifts up or down. It just redraws the current menu.
def update_menu():
	draw_menu(current_menu)

#Draws cursor next to current selection
def draw_cursor():
	print("sel = " + str(sel))
	print("frame_shift = " + str(frame_shift))
	lcd.write_string(" ")
	lcd.cursor_pos = (sel - frame_shift,0)
	lcd.write_string("*")
	lcd.cursor_pos = (sel - frame_shift,0)

#Writes an informative message to the screen for a specified amount of time
#If delay is 0, the message will stay indefinitely until the screen is cleared manually
def message(message, delay):
	print("message")
	lcd.clear()
	lcd.cursor_pos = (0,0)
	lcd.write_string(message)
	lcd.cursor_pos = (0,0)
	if (delay > 0):
		time.sleep(delay)
		update_menu()
		draw_cursor()
#Polling code for inputs
def loop():
	#various variables for the polling loop
	a = 0
	b = 0
	btn = 0
	a_old = 0
	b_old = 0
	btn_old = 0
	rot_state = 0

	while True:
		#read pin status
		a = GPIO.read(pin_rot_a)
		b = GPIO.read(pin_rot_b)
		btn = GPIO.read(pin_rot_btn)
	
		#check if any of the pins have changed
		if (a != a_old or b!= b_old or btn != btn_old):
			#print(str(a) + str(b))

			if (btn == 0):
				ui_select()
				time.sleep(0.5) #debounce
		
			#Once we receive a 11 from the rotary encoder, set state to 1
			#After that, check if we get 01 or 10 for CW and CCW respectively
			if (a == 1 and b == 1):
				rot_state = 1
			elif (rot_state == 1 and a == 0 and b == 1):
				print("clockwise")
				ui_up()
				time.sleep(0.01)	#debounce
				rot_state = 0
			elif (rot_state == 1 and a == 1 and b == 0):
				print("counter clockwise")
				ui_down()
				time.sleep(0.01)	#debounce
				rot_state = 0
		a_old = a
		b_old = b
		btn_old = btn

#disable annoying logging messages
logging.disable('DEBUG')

#uartCom = ""

#pin definitions
#You have to look these up in the BBone docs, there's not a clear relastionship between these numbers and the physical pins on the board
pin_rot_a = 193		#P8_5
pin_rot_b = 194		#P8_6
pin_rot_btn = 25 	#P8_4

#UI global variables
ui_state = "menu"	#current UI state
sel = 0			#Current selection
max_sel = 6		#Number of items in menu
frame_shift = 0		#shift the "frame" down by this many lines for menus that don't fit on the LCD
current_menu = [""]	#global to store data of current menu

#File Directories
sd_base = "/media/debian/2857-A65B"	#Base directory pointing to the inserted SD Card
json_dir = "/cfg/json"			#JSON configuration directory, relative to SD base directory
chirp_dir = "/cfg/chirp"		#Chirp configuration directory, relative to SD base directory

#Config
json_file_path = "NONE"		#Full path to currently selected json file
chirp_file_path = "NONE"	#Full path to currently selected chirp file

#Run setup functions, draw the main menu, and start polling for inputs
gpio_setup()
lcd_setup()
draw_main_menu()
loop()
