import os
import sys
import json
import time
import logging
import datetime
import subprocess
import configparser

# Tkinter
from tkinter import *
from tkinter import messagebox
from tkcalendar import *

# CustomTkinter
import customtkinter
customtkinter.set_appearance_mode("dark")

# Resolution
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

# Image Library
from PIL import Image, ImageTk

# - Global Variables - #
LOG = ""

# Tkinter Varibles
ROOT = customtkinter.CTk()
TKINTER_WIDGETS = {}
TKINTER_DATA = {}
APP_WIDTH = 270
APP_HEIGHT = 300

# Current Script Name
CURRENT_SCRIPT_NAME = os.path.basename(__file__).split('.')[0]

# Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Config")
IMAGES_DIRECTORY = os.path.join(CONFIG_DIRECTORY, "Images")
LOGS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Logs")

# Config
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(CONFIG_DIRECTORY, f"{CURRENT_SCRIPT_NAME}.cfg"))


# Logger
def logger():
    
    global LOG

    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(funcName)s : %(lineno)d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    # Current Year-Month
    current_year_month = datetime.datetime.now().strftime("%Y-%m")

    # Logger file name
    log_file_name = f"{current_year_month}_{CURRENT_SCRIPT_NAME}.log"

    # Create Logs Folder if it does not exist
    os.makedirs(LOGS_DIRECTORY, exist_ok=True)

    # Log file path
    log_file = os.path.join(LOGS_DIRECTORY, log_file_name)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    LOG.addHandler(file_handler)
    
    # StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    LOG.addHandler(stream_handler)


# Quit Homepage
def quit_homepage():
    LOG.debug("- Quit Homepage -")

    global ROOT
    
    # Quit Homepage
    ROOT.destroy()


# Exit Bot
def exit_bot():
    LOG.debug("- Exit Bot -")

    # Quit Homepage
    quit_homepage()

    # Exit
    LOG.debug("Exit Bot")
    sys.exit(0)


# Post Top Level Select Date Time
def post_top_level_select_date_time():
    global TKINTER_WIDGETS
    
    # Destroy Top Level Date Time
    TKINTER_WIDGETS['top_level_date_time'].destroy()

    # Activate Button Select Date Time
    TKINTER_WIDGETS['btn_select_date_time'].configure(state=NORMAL)


# Scroll Hours
def scroll_hours(event):
    global TKINTER_WIDGETS
    global TKINTER_DATA

    current_index = TKINTER_DATA['values_hours'].index(TKINTER_DATA['string_var_hours'].get())

    if event.delta > 0:
        if current_index < len(TKINTER_DATA['values_hours'])-1:
            current_index += 1
        else:
            current_index = 0
    else:
        current_index -= 1
    
    TKINTER_DATA['string_var_hours'].set(TKINTER_DATA['values_hours'][current_index])
    TKINTER_WIDGETS['spinbox_hours'].config(textvariable=TKINTER_DATA['string_var_hours'])


# Scroll Minutes
def scroll_minutes(event):
    global TKINTER_WIDGETS
    global TKINTER_DATA

    current_index = TKINTER_DATA['values_minutes'].index(TKINTER_WIDGETS['spinbox_minutes'].get())

    if event.delta > 0:
        if current_index < len(TKINTER_DATA['values_minutes'])-1:
            current_index += 1
        else:
            current_index = 0
    else:
        current_index -= 1
    
    TKINTER_DATA['string_var_minutes'].set(TKINTER_DATA['values_minutes'][current_index])
    TKINTER_WIDGETS['spinbox_minutes'].config(textvariable=TKINTER_DATA['string_var_minutes'])


# Update Date Time
def update_date_time():
    global TKINTER_DATA
    global TKINTER_WIDGETS

    # Get New Date Time Details
    new_date = TKINTER_WIDGETS['CAL'].get_date()
    # new_time = f'{TKINTER_DATA["string_var_hours"].get()}:{TKINTER_DATA["string_var_minutes"].get()}'
    new_time = f'{TKINTER_WIDGETS["spinbox_hours"].get()}:{TKINTER_WIDGETS["spinbox_minutes"].get()}'

    # Destroy Top Level Widget
    post_top_level_select_date_time()

    # Update Date Entry
    TKINTER_WIDGETS['entry_date'].configure(state=NORMAL)
    TKINTER_WIDGETS['entry_date'].delete(0, END)
    TKINTER_WIDGETS['entry_date'].insert(0, new_date)
    TKINTER_WIDGETS['entry_date'].configure(state=DISABLED)

    # Update Time Entry
    TKINTER_WIDGETS['entry_time'].configure(state=NORMAL)
    TKINTER_WIDGETS['entry_time'].delete(0, END)
    TKINTER_WIDGETS['entry_time'].insert(0, new_time)
    TKINTER_WIDGETS['entry_time'].configure(state=DISABLED)


# Select Date Time
def select_date_time():
    
    global TKINTER_WIDGETS
    global TKINTER_DATA
    global ROOT

    # Disable Button Select EID
    TKINTER_WIDGETS['btn_select_date_time'].configure(state=DISABLED)
    
    # Create Top Level Window
    TKINTER_WIDGETS['top_level_date_time'] = customtkinter.CTkToplevel(takefocus=True)

    # Properties
    TKINTER_WIDGETS['top_level_date_time'].title("Select Date / Time")
    # TKINTER_WIDGETS['top_level_date_time'].iconbitmap(os.path.join(IMAGES_DIRECTORY, CONFIG.get('tkinter', 'icon')))
    
    # Size
    top_level_date_time_width = 300
    top_level_date_time_height = 350

    screen_width = ROOT.winfo_screenwidth()
    screen_height = ROOT.winfo_screenheight()

    app_center_coordinate_x = (screen_width / 3) - (top_level_date_time_width / 2.5)
    app_center_coordinate_y = (screen_height / 3) - (top_level_date_time_height / 2.5)

    # Position App to the Centre of the Screen
    TKINTER_WIDGETS['top_level_date_time'].geometry(f"{top_level_date_time_width}x{top_level_date_time_height}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")

    # Prevent User from Resizing the Window
    TKINTER_WIDGETS['top_level_date_time'].resizable(width=False, height=False)

    # Close 'X' Button
    TKINTER_WIDGETS['top_level_date_time'].protocol("WM_DELETE_WINDOW", post_top_level_select_date_time)

    TKINTER_WIDGETS['top_level_date_time'].grid_rowconfigure(1, weight=1)
    TKINTER_WIDGETS['top_level_date_time'].grid_columnconfigure(0, weight=1)

    # - Top Level Select Date / Time Design - #

    # Frame Calendar
    frame_calendar = customtkinter.CTkFrame(master=TKINTER_WIDGETS['top_level_date_time'], corner_radius=10)
    frame_calendar.grid(row=0, column=0, padx=15, pady=15, columnspan=3)

    # Label Date
    TKINTER_WIDGETS['label_date'] =  customtkinter.CTkLabel(master=frame_calendar, text="- Select Date -", width=30, height=5, corner_radius=7)
    TKINTER_WIDGETS['label_date'].grid(row=0, column=0, padx=10, pady=5, columnspan=3, sticky='n')

    # Calendar
    TKINTER_WIDGETS['CAL'] = Calendar(frame_calendar, selectmode='day', date_pattern='dd/mm/y', mindate=datetime.datetime.today())
    TKINTER_WIDGETS['CAL'].grid(row=0, column=0, padx=20, pady=30, columnspan=3, sticky='s')

    # Frame Time
    frame_time = customtkinter.CTkFrame(master=TKINTER_WIDGETS['top_level_date_time'], corner_radius=10)
    frame_time.grid(row=1, column=0, padx=15, pady=5, columnspan=3)

    # Time
    # Label Time
    TKINTER_WIDGETS['label_time'] =  customtkinter.CTkLabel(master=frame_time, text="Time", width=30, height=5, corner_radius=7)
    # TKINTER_WIDGETS['label_time'].grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky='n')
    TKINTER_WIDGETS['label_time'].grid(row=0, column=0, padx=10, pady=10)

    # Hours
    TKINTER_DATA['values_hours'] = ['00']

    for i in range(1, 24):
        if len(str(i)) == 1:
            TKINTER_DATA['values_hours'].append(f'0{str(i)}')
        else:
            TKINTER_DATA['values_hours'].append(str(i))
        i+=1
    
    TKINTER_DATA['values_hours'] = tuple(TKINTER_DATA['values_hours'])
    
    # SpinBox Hours
    TKINTER_WIDGETS['spinbox_hours'] = Spinbox(frame_time, values=TKINTER_DATA['values_hours'], justify=CENTER, width=10, wrap=True)
    TKINTER_WIDGETS['spinbox_hours'].grid(row=0, column=1, padx=10)
    TKINTER_WIDGETS['spinbox_hours'].bind("<MouseWheel>", scroll_hours)

    # Set Default Value
    TKINTER_DATA['string_var_hours'] = StringVar()
    TKINTER_DATA['string_var_hours'].set(CONFIG.get('tkinter', 'default_time').split(':')[0])
    TKINTER_WIDGETS['spinbox_hours'].config(textvariable=TKINTER_DATA['string_var_hours'])

    TKINTER_DATA['values_minutes'] = ['00']

    for i in range(1, 60):
        if len(str(i)) == 1:
            TKINTER_DATA['values_minutes'].append(f'0{str(i)}')
        else:
            TKINTER_DATA['values_minutes'].append(str(i))
        i+=1
    
    TKINTER_DATA['values_minutes'] = tuple(TKINTER_DATA['values_minutes'])

    # SpinBox Minutes
    TKINTER_WIDGETS['spinbox_minutes'] = Spinbox(frame_time, values=TKINTER_DATA['values_minutes'], justify=CENTER, width=10, wrap=True)
    TKINTER_WIDGETS['spinbox_minutes'].grid(row=0, column=2, padx=10)
    TKINTER_WIDGETS['spinbox_minutes'].bind("<MouseWheel>", scroll_minutes)

    # TextVariable for Minutes
    TKINTER_DATA['string_var_minutes'] = StringVar()

    # Button Select Date Time OK
    TKINTER_WIDGETS['button_select_date_time_ok'] = customtkinter.CTkButton(master=TKINTER_WIDGETS['top_level_date_time'], text="OK", width=70, command=update_date_time)
    TKINTER_WIDGETS['button_select_date_time_ok'].grid(row=2, column=0, padx=60, pady=15, sticky='sw')

    # Button Select Date Time Cancel
    TKINTER_WIDGETS['button_select_date_time_cancel'] = customtkinter.CTkButton(master=TKINTER_WIDGETS['top_level_date_time'], text="Cancel", fg_color="gray74", hover_color="#EEE", text_color="#000", width=70, command=post_top_level_select_date_time)
    TKINTER_WIDGETS['button_select_date_time_cancel'].grid(row=2, column=0, padx=60, pady=15, sticky='se')


# Validate Entries
def validate_entries():

    global TKINTER_WIDGETS
    global TKINTER_DATA
    
    # Email
    if TKINTER_WIDGETS["entry_email"].get() == "":
        messagebox.showerror("Bot Error", "'Email' cannot be blank.")
        return
    
    '''
    # Check for Valid Email
    # email_regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
    email_regex = '^[a-zA-Z0-9]+([\._]?[a-zA-Z0-9])*[@]\w+[.]\w{2,3}$'
    if not (re.search(email_regex, TKINTER_WIDGETS["entry_email"].get())):
        messagebox.showerror("Bot Error", "Please enter a valid email.")
        return
    # '''

    # Name
    if TKINTER_WIDGETS["entry_name"].get() == "":
        messagebox.showerror("Bot Error", "'Name' cannot be blank.")
        return

    # Assign Variables
    deadline_date = TKINTER_WIDGETS['entry_deadline_date'].get()
    deadline_date_obj = datetime.datetime.strptime(deadline_date, '%Y-%m-%d')

    deadline_day = deadline_date_obj.strftime('%d')

    if deadline_day[1] == "1":
        TKINTER_DATA['deadline_date'] = deadline_date_obj.strftime('%A, %#d<sup>st</sup> %B %Y')
    elif deadline_day[1] == "2":
        TKINTER_DATA['deadline_date'] = deadline_date_obj.strftime('%A, %#d<sup>nd</sup> %B %Y')
    elif deadline_day[1] == "3":
        TKINTER_DATA['deadline_date'] = deadline_date_obj.strftime('%A, %#d<sup>rd</sup> %B %Y')
    else:
        TKINTER_DATA['deadline_date'] = deadline_date_obj.strftime('%A, %#d<sup>th</sup> %B %Y')

    TKINTER_DATA['email'] = TKINTER_WIDGETS["entry_email"].get()
    TKINTER_DATA['name'] = TKINTER_WIDGETS["entry_name"].get()

    LOG.debug(f"Deadline Date: {TKINTER_DATA['deadline_date']}")
    LOG.debug(f"Email: {TKINTER_DATA['email']}")
    LOG.debug(f"Name: {TKINTER_DATA['name']}")
    
    # Quit Homepage & Execute Bot
    quit_homepage()


# Homepage
def homepage():
    LOG.debug("- Homepage -")

    global ROOT
    global TKINTER_WIDGETS

    try:
        # Read the Image
        img = Image.open(os.path.join(IMAGES_DIRECTORY, "python-logo.png"))
        img_resized = img.resize((100, 100))
        img = ImageTk.PhotoImage(img_resized)

        TKINTER_WIDGETS['label_img'] = customtkinter.CTkLabel(master=ROOT, image=img, corner_radius=7)
        TKINTER_WIDGETS['label_img'].image = img
        TKINTER_WIDGETS['label_img'].grid(row=0, column=0, columnspan=2, padx=15, pady=10)

        # - Frame Details - #
        frame_details = customtkinter.CTkFrame(master=ROOT, corner_radius=10)
        frame_details.grid(row=1, column=0, padx=15, pady=15)
        frame_details.grid_rowconfigure(1, weight=1)
        frame_details.grid_columnconfigure(0, weight=1)
        ROOT.grid_rowconfigure(1, weight=1)
        ROOT.grid_columnconfigure(0, weight=1)
        
        # Label Date
        TKINTER_WIDGETS['label_date'] = customtkinter.CTkLabel(master=frame_details, text="Date", width=30, height=25, corner_radius=7)
        TKINTER_WIDGETS['label_date'].grid(row=0, column=0, padx=10, pady=20)

        # Current Date Time
        current_date_time = datetime.datetime.now().strftime('%d/%m/%Y')

        # Entry Date
        TKINTER_WIDGETS['entry_date'] = customtkinter.CTkEntry(master=frame_details, width=90, height=30, border_width=2, corner_radius=10)
        TKINTER_WIDGETS['entry_date'].insert(0, current_date_time)
        TKINTER_WIDGETS['entry_date'].configure(state=DISABLED)
        TKINTER_WIDGETS['entry_date'].grid(row=0, column=1, padx=10, sticky='w')

        # Label Time
        TKINTER_WIDGETS['label_time'] = customtkinter.CTkLabel(master=frame_details, text="Time", width=30, height=25, corner_radius=7)
        TKINTER_WIDGETS['label_time'].grid(row=1, column=0)

        # Entry Time
        TKINTER_WIDGETS['entry_time'] = customtkinter.CTkEntry(master=frame_details, width=90, height=30, border_width=2, corner_radius=10, justify=CENTER)
        TKINTER_WIDGETS['entry_time'].insert(0, CONFIG.get('tkinter', 'default_time'))
        TKINTER_WIDGETS['entry_time'].configure(state=DISABLED)
        TKINTER_WIDGETS['entry_time'].grid(row=1, column=1, padx=10)

        # Button Select Date Time
        TKINTER_WIDGETS['btn_select_date_time'] = customtkinter.CTkButton(master=frame_details, text="Select Date/Time", width=150, command=select_date_time)
        TKINTER_WIDGETS['btn_select_date_time'].grid(row=2, column=0, columnspan=2, padx=10, pady=15)

    except Exception as e:
        LOG.error("Failed")
        LOG.error(e, exc_info=True)


# Load UI
def load_ui():
    LOG.debug("- Load UI -")

    global ROOT

    # Properties
    ROOT.title(CONFIG.get('tkinter', 'title'))
    # ROOT.iconbitmap(os.path.join(IMAGES_DIRECTORY, CONFIG.get('tkinter', 'icon')))

    homepage()

    #  - Set Window to appear in the middle when program runs -
    screen_width = ROOT.winfo_screenwidth()
    screen_height = ROOT.winfo_screenheight()

    app_center_coordinate_x = (screen_width / 3) - (APP_WIDTH / 2.5)
    app_center_coordinate_y = (screen_height / 3) - (APP_HEIGHT / 2.5)

    # Position App to the Centre of the Screen
    ROOT.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")

    # Prevent User from Resizing the Window
    # ROOT.resizable(width=False, height=False)

    # Close 'X' Button
    ROOT.protocol("WM_DELETE_WINDOW", exit_bot)

    # Infinite Loop
    ROOT.mainloop()


# Main
if __name__ == "__main__":
    logger()

    LOG.debug("--- Start ---")

    try:
        # Load UI
        load_ui()

    except Exception as e:
        LOG.error("Failed")
        LOG.error(e, exc_info=True)
    
    finally:
        LOG.debug("--- End ---")