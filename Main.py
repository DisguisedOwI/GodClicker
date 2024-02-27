import time
import keyboard
import win32api
import win32con
import customtkinter as ctk
import threading
from PIL import Image, ImageTk

# Variable to track auto-click status
auto_click_on = False
auto_click_thread = None

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Function to perform mouse click


def click():
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
        auto_click_button.configure(text="Stop Auto Click")
        start_auto_click_thread()
        update_button_text()
    else:
        auto_click_button.configure(text="Start Auto Click")

# Function to start the auto-clicking thread
def start_auto_click_thread():
    global auto_click_thread
    auto_click_thread = threading.Thread(target=perform_auto_click_thread)
    auto_click_thread.daemon = True
    auto_click_thread.start()

# Function to perform auto-clicking in a separate thread
def perform_auto_click_thread():
    while auto_click_on:
        click()
        time.sleep(auto_click_delay)


# Function to update button text dynamically
def update_button_text():
    if auto_click_on:
        auto_click_button.after(1000, update_button_text)
        last_name = "Auto Clicking..."
        auto_click_button.configure(text=f"Stop {last_name}")
    else:
        auto_click_button.configure(text="Start Auto Click")

# Handle F6 key press event
def handle_f6_press(event):
    toggle_auto_click()


def on_image_click():
    import webbrowser
    webbrowser.open("https://github.com/DisguisedOwI")


# Create the main application window
app = ctk.CTk()
app.geometry("400x170")
app.title("God Clicker")
app.iconbitmap("_internal\\icons\\LogoV2.ico")

# Make the window not resizable
app.resizable(False, False)


# Create the Auto Click button
auto_click_button = ctk.CTkButton(
    app, text="Start Auto Click", command=toggle_auto_click)
auto_click_button.pack(pady=20)

# Create a canvas to display the image
Image_import_button_icon = Image.open("_internal\\icons\\github.png")  # Load the icon image
Image_import_button_icon = Image_import_button_icon.resize((20, 20))  # Resize the icon as needed
Image_import_button_icon = ctk.CTkImage(Image_import_button_icon)

Github_button = ctk.CTkButton(app, text="", command=on_image_click, image=Image_import_button_icon, width=20, height=20)
Github_button.place(x=10, y=135)


# Create the Hours label and entry
delay_label = ctk.CTkLabel(app, text="Hours")
delay_label.place(x=102, y=95)

delay_entry_Hours= ctk.CTkEntry(app, width=50)
delay_entry_Hours.place(x=95 + 0 * 55, y=70)

# Create the Minutes label and entry
delay_label = ctk.CTkLabel(app, text="Mins")
delay_label.place(x=102+58, y=95)

delay_entry_Minutes= ctk.CTkEntry(app, width=50)
delay_entry_Minutes.place(x=95 + 1 * 55, y=70)

# Create the Seconds label and entry
delay_label = ctk.CTkLabel(app, text="Secs")
delay_label.place(x=102+58+55, y=95)

delay_entry_Seconds= ctk.CTkEntry(app, width=50)
delay_entry_Seconds.place(x=95 + 2 * 55, y=70)

# Create the Delay label and entry
delay_label = ctk.CTkLabel(app, text="Millis.")
delay_label.place(x=102+58+56+54, y=95)

initial_millis_text = "500"  # Change this to the desired initial text
delay_entry_Millis = ctk.CTkEntry(app, width=50)
delay_entry_Millis.insert(0, initial_millis_text)  # Set initial text
delay_entry_Millis.place(x=95 + 3 * 55, y=70)


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


# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Set the appearance mode to dark

# Start the application event loop
app.mainloop()
