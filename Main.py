import time
import keyboard
import win32api
import win32con
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import random

# Variable to track auto-click status
auto_click_on = False
auto_click_thread = None
auto_click_delay = 0  # Initialize auto_click_delay globally
offset_checked = False

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

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

# Function to perform auto-clicking in a separate thread
def perform_auto_click_thread():
    while auto_click_on:
        click()
        time.sleep(auto_click_delay)
        if offset_checked:  # Check if the Offset checkbox is checked
            random_delay = random.uniform(0, float(delay_entry_Offset.get()) / 1000)
            time.sleep(random_delay)

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
    webbrowser.open("https://github.com/DisguisedOwI")

# Create the main application window
app = ctk.CTk()
app.geometry("400x170")
app.title("God Clicker")
app.iconbitmap("_internal\\icons\\LogoV4.ico")

# Make the window not resizable
app.resizable(False, False)

# Create the Auto Click button
auto_click_button = ctk.CTkButton(
    app, text="Start Auto Click (F6)", command=toggle_auto_click)
auto_click_button.place(x=10, y=135)

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
delay_label = ctk.CTkLabel(app, text="Millis.")
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
Right_Click.place(x=15, y=85)

#----------------------------------------------

# Create the Delay label and entry
delay_label = ctk.CTkLabel(app, text="Millis.")
delay_label.place(x=135+V, y=55)

delay_entry_Offset = ctk.CTkEntry(app, width=50, height=20)
initial_Offset_text = "40"  # Change this to the desired initial text
delay_entry_Offset.insert(0, initial_Offset_text)  # Set initial text
delay_entry_Offset.place(x=135, y=55)

# Create a canvas to display the image
Image_import_button_icon = Image.open("_internal\\icons\\github.png")  # Load the icon image
Image_import_button_icon = Image_import_button_icon.resize((20, 20))  # Resize the icon as needed
Image_import_button_icon = ctk.CTkImage(Image_import_button_icon)

Github_button = ctk.CTkButton(app, text="", command=on_image_click, image=Image_import_button_icon, width=20, height=20)
Github_button.place(x=355, y=135)

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

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Set the appearance mode to dark

# Start the application event loop
app.mainloop()
