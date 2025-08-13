import time
import keyboard
import win32api
import win32con
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import random
import requests
import tkinter as tk
from mousekey import MouseKey
import io
import tempfile

mkey = MouseKey()

# Variable to track auto-click status
auto_click_on = False 				# Variable to track right-click status
auto_click_thread = None 	# Thread for auto-clicking
auto_click_delay = 0  				# Initialize auto_click_delay globally
offset_checked = False 			# Variable to track offset checkbox status
repeat_checked = False 			# Variable to track repeat checkbox status
auto_click_delay = 0.5  			# Default delay in seconds
current_version="4.0" 			# Current version of the application
window_width = 400 			# Width of the main window
window_height = 270 			# Height of the main window


# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



def check_for_updates():
	try:
		# Get the latest release from the GitHub API
		release_url="https://api.github.com/repos/DisguisedOwI/GodClicker/releases/latest"
		release_data=requests.get(release_url).json()	# Get the release data
		latest_version=release_data["tag_name"]			# Get the latest version number
		latest_version=latest_version[1:]  				# Remove the "v" from the version number
		return latest_version							# Return the latest version number

	except Exception as e:
		print(f"Error checking for updates: {e}")		# Print the error message
		return "0.0"									# Return 0.0 if an error occurs


# Function to perform mouse click

def toggle_right_click():
	global right_click_enabled
	right_click_enabled = not right_click_enabled

def click():
	if right_click_enabled:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# Function to start/stop auto-clicking
def toggle_auto_click():
	global auto_click_on, auto_click_thread
	auto_click_on = not auto_click_on
	
	# Check if the auto-click thread exists and is alive
	if auto_click_thread and auto_click_thread.is_alive():
		auto_click_thread.join()  # Terminate the previous thread
	
	if auto_click_on:
		auto_click_button.configure(text="Stop Auto Click (F6)")
		start_auto_click_thread()
		update_button_text()
	else:
		auto_click_button.configure(text="Start Auto Click (F6)")

# Function to start the auto-clicking thread
def start_auto_click_thread():
	global auto_click_thread
	auto_click_thread = threading.Thread(target=perform_auto_click_thread)
	auto_click_thread.daemon = True
	auto_click_thread.start()

def toggle_offset():
	global offset_checked
	offset_checked = not offset_checked

def toggle_repeat():
	global repeat_checked
	repeat_checked = not repeat_checked
	print(f"Repeat is now {'enabled' if repeat_checked else 'disabled'}")

# Function to perform auto-clicking in a separate thread
def perform_auto_click_thread():
	if offset_checked:  # Check if the Offset checkbox is checked
		while auto_click_on:
			click()
			time.sleep(auto_click_delay)
			if offset_checked:  # Check if the Offset checkbox is checked
				random_delay = random.uniform(0, float(delay_entry_Offset.get()) / 1000)
				time.sleep(random_delay)

	elif repeat_checked:  # Check if the Repeat checkbox is checked
		repeat_times = int(Repeat_times.get())
		for _ in range(repeat_times):
			if not auto_click_on:
				break
			click()
			time.sleep(auto_click_delay)
			if offset_checked:
				random_delay = random.uniform(0, float(delay_entry_Offset.get()) / 1000)
				time.sleep(random_delay)

	#if everything delay is 0, then stop clicking
	elif auto_click_delay == 0:
		while auto_click_on:
			click()  # Perform a single click if delay is 0

	else:
		while auto_click_on:
			click()
			time.sleep(auto_click_delay)

# Function to update button text dynamically
def update_button_text():
	if auto_click_on:
		auto_click_button.after(1000, update_button_text)
		last_name = "Auto Clicking... (F6)"
		auto_click_button.configure(text=f"Stop {last_name}")
	else:
		auto_click_button.configure(text="Start Auto Click (F6)")

# Handle F6 key press event
def handle_f6_press(event):
	toggle_auto_click()

# The Creator GitHub
def on_image_click():
	import webbrowser
	webbrowser.open("https://github.com/DisguisedOwI/GodClicker")

# Create the main application window

# GitHub raw URL for the .ico file
ICON_URL = "https://raw.githubusercontent.com/DisguisedOwI/GodClicker/main/_internal/icons/logoV4.ico"

# Download the icon
response = requests.get(ICON_URL)
response.raise_for_status()  # Ensure it downloaded correctly

# Save to a temporary file
tmp_icon = tempfile.NamedTemporaryFile(delete=False, suffix=".ico")
tmp_icon.write(response.content)
tmp_icon.close()

app = ctk.CTk()
app.geometry(f"{int(window_width)}x{int(window_height)}")  # Set the window size
app.title("God Clicker")
app.iconbitmap(tmp_icon.name)

# Make the window not resizable
app.resizable(False, False)


#my_image = ctk.CTkImage(light_image=Image.open('Test.png'),
#	dark_image=Image.open('Test.png'),
#	size=(400, 270))  # Load the image and set its size

#my_label = ctk.CTkLabel(app, text="", image=my_image)
#my_label.pack(pady=0, padx=0, fill=tk.BOTH, expand=True)  # Add the image label to the window


# Create the Auto Click button
auto_click_button = ctk.CTkButton(
	app, text="Start Auto Click (F6)", command=toggle_auto_click)
auto_click_button.place(relx=0.188, rely=0.93, anchor=tk.CENTER)  # Center the button in the window

#----------------------------------------------

N = 12.5  # Initial x position of the first label and entry
H = 95  # Horizontal distance between the labels and entries
V = 55  # Vertical distance between the labels and entries

Hx, Hy = N + 0 * H, 15
Mx, My = N + 1 * H, 15
Sx, Sy = N + 2 * H, 15
Mix, Miy = N + 3 * H, 15

#----------------------------------------------

# Create the Hours label and entry
delay_label = ctk.CTkLabel(app, text="Hours")
delay_label.place(x=Hx+V, y=Hy)

delay_entry_Hours= ctk.CTkEntry(app, width=50)
initial_Hours_text = "0"  # Change this to the desired initial text
delay_entry_Hours.insert(0, initial_Hours_text)  # Set initial text
delay_entry_Hours.place(x=Hx, y=Hy)

#----------------------------------------------

# Create the Minutes label and entry
delay_label = ctk.CTkLabel(app, text="Mins")
delay_label.place(x=Mx+V, y=My)

delay_entry_Minutes= ctk.CTkEntry(app, width=50)
initial_minutes_text = "0"  # Change this to the desired initial text
delay_entry_Minutes.insert(0, initial_minutes_text)  # Set initial text
delay_entry_Minutes.place(x=Mx, y=My)

#----------------------------------------------

# Create the Seconds label and entry
delay_label = ctk.CTkLabel(app, text="Secs")
delay_label.place(x=Sx+V, y=Sy)

delay_entry_Seconds= ctk.CTkEntry(app, width=50)
initial_seconds_text = "0"  # Change this to the desired initial text
delay_entry_Seconds.insert(0, initial_seconds_text)  # Set initial text
delay_entry_Seconds.place(x=Sx, y=Sy)

#----------------------------------------------

# Create the Delay label and entry
delay_label = ctk.CTkLabel(app, text="Millis")
delay_label.place(x=Mix+V, y=Miy)

delay_entry_Millis = ctk.CTkEntry(app, width=50)
initial_millis_text = "500"  # Change this to the desired initial text
delay_entry_Millis.insert(0, initial_millis_text)  # Set initial text
delay_entry_Millis.place(x=Mix, y=Miy)

#----------------------------------------------

# Random offset
Offset = ctk.CTkCheckBox(app, text="Random Offset", checkbox_width=20, checkbox_height=20, corner_radius=5, border_width=2.5)
#size = (20, 20)
Offset.place(x=15, y=55)

#----------------------------------------------

# Right Click toggle checkbox
right_click_enabled = False
Right_Click = ctk.CTkCheckBox(app, text="Right Click", checkbox_width=20, checkbox_height=20, corner_radius=5, border_width=2.5, command=toggle_right_click)
Right_Click.place(x=15, y=135)

#----------------------------------------------

# Create the Delay label and entry
delay_label = ctk.CTkLabel(app, text="Millis")
delay_label.place(x=135+V, y=55)

delay_entry_Offset = ctk.CTkEntry(app, width=50, height=20)
initial_Offset_text = "40"  # Change this to the desired initial text
delay_entry_Offset.insert(0, initial_Offset_text)  # Set initial text
delay_entry_Offset.place(x=135, y=55)

#----------------------------------------------

Repeat = ctk.CTkCheckBox(app, text="Repeat", checkbox_width=20, checkbox_height=20, corner_radius=5, border_width=2.5)
#size = (20, 20)
Repeat.place(x=15, y=85)

# Create the Delay label and entry
delay_label = ctk.CTkLabel(app, text="Times")
delay_label.place(x=135+V, y=85)

Repeat_times= ctk.CTkEntry(app, width=50, height=20)
Repeat_times_text = "10"  # Change this to the desired initial text
Repeat_times.insert(0, Repeat_times_text)  # Set initial text
Repeat_times.place(x=135, y=85)


# URL to the raw image file on GitHub
image_url = "https://raw.githubusercontent.com/DisguisedOwI/GodClicker/main/_internal/icons/github.png"

# Download the image
response = requests.get(image_url)
response.raise_for_status()  # Raise an error if download fails

# Load the image into PIL from bytes
image_data = io.BytesIO(response.content)
Image_import_button_icon = Image.open(image_data)
Image_import_button_icon = Image_import_button_icon.resize((20, 20))
Image_import_button_icon = ctk.CTkImage(Image_import_button_icon)

# Create the button
Github_button = ctk.CTkButton(app, text="", command=on_image_click, image=Image_import_button_icon, width=20, height=20)
Github_button.place(relx=0.94, rely=0.93, anchor=tk.CENTER)


# Function to handle the GitHub button click
latest_version=check_for_updates()

if latest_version!=current_version:
	print(f"Current version: {current_version}")
	print(f"Latest version: {latest_version}")
	print("An update is available!")

	Update_text=ctk.CTkButton(app,text="Update Available!",font=("Arial",12,"underline","italic"),command=on_image_click,fg_color="#242424",hover_color="#242424",width=20,height=10)
	Update_text.place(relx=0.75,rely=0.94,anchor=tk.CENTER)

	


# Function to update auto click delay when the entry value changes
def update_auto_click_delay():
	global auto_click_delay
	
	# Get the values from the entry widgets and convert them to seconds
	try:
		hours = float(delay_entry_Hours.get()) * 3600
	except ValueError:
		hours = 0
		
	try:
		minutes = float(delay_entry_Minutes.get()) * 60
	except ValueError:
		minutes = 0
		
	try:
		seconds = float(delay_entry_Seconds.get())
	except ValueError:
		seconds = 0
		
	try:
		millis = float(delay_entry_Millis.get()) / 1000
	except ValueError:
		millis = 0

	# If milliseconds is 0, set auto_click_delay to 0
	if millis and seconds and minutes and hours == 0:
		auto_click_delay = 0
	else:
		# Calculate the total delay
		auto_click_delay = hours + minutes + seconds + millis


# Bind F6 key press event to start/stop auto-clicking
keyboard.on_press_key("F6", handle_f6_press)

# Bind the update_auto_click_delay function to entry value changes
delay_entry_Hours.bind("<KeyRelease>", lambda event: update_auto_click_delay())
delay_entry_Minutes.bind("<KeyRelease>", lambda event: update_auto_click_delay())
delay_entry_Seconds.bind("<KeyRelease>", lambda event: update_auto_click_delay())
delay_entry_Millis.bind("<KeyRelease>", lambda event: update_auto_click_delay())

Offset.configure(command=toggle_offset)
Repeat.configure(command=toggle_repeat)

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Set the appearance mode to dark

# Start the application event loop
app.mainloop()
