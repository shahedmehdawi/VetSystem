from tkinter import *
from tkinter import ttk  
from customtkinter import *
from PIL import Image

#test
app = CTk()
app.geometry("800x600")
app.resizable(0, 0)

side_img_data = Image.open("cybersecurity.jpg")
email_icon_data = Image.open("email-icon.png")
password_icon_data = Image.open("password-icon.png")
google_icon_data = Image.open("google-icon.png")
doctor_icon_data = Image.open("doctor.png")


side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 600))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(25, 25))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(20, 20))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(20, 20))
doctor_icon = CTkImage(dark_image=doctor_icon_data, light_image=doctor_icon_data, size=(20, 20))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=400, height=600, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Welcome Admin", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 30)).pack(anchor="w", pady=(40, 10), padx=(50, 0))
CTkLabel(master=frame, text=" Let's Register!", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(0,0), padx=(50, 0))

CTkLabel(master=frame, text="  Username:", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 16), image=doctor_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(50, 0))
CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#A1045A", border_width=1, text_color="#000000").pack(anchor="w", padx=(50, 0))

CTkLabel(master=frame, text="  Password:", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 16), image=password_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(50, 0))
CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#A1045A", border_width=1, text_color="#000000", show="*").pack(anchor="w", padx=(50, 0))

CTkLabel(master=frame, text="  Name:", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 16), image=doctor_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(50, 0))
CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#A1045A", border_width=1, text_color="#000000").pack(anchor="w", padx=(50, 0))

CTkLabel(master=frame, text="  Email:", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 16), image=email_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(50, 0))
CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#A1045A", border_width=1, text_color="#000000").pack(anchor="w", padx=(50, 0))

# Dropdown menu with custom style

def enable_submit(*args):
    if clicked.get() != "Choose one":
        submit_button.configure(state="normal")
    else:
        submit_button.configure(state="disabled")


label = CTkLabel(master=frame, text="Select an option:", text_color="#A1045A", font=("Arial Bold", 16))
label.pack(anchor="w", pady=(30, 0), padx=(50, 0))

options = ["Choose one", "Doctor", "User", "Admin"]
clicked = StringVar() 
clicked.set("Choose one")
clicked.trace_add("write", enable_submit)  

style = ttk.Style()
style.theme_use('clam')  


style.configure('Custom.TMenubutton', foreground='#A1045A', font=('Arial Bold', 14), arrowcolor='#A1045A', relief='flat')

drop = ttk.OptionMenu(frame, clicked, *options, style='Custom.TMenubutton')  
drop.pack()

submit_button = CTkButton(master=frame, text="Submit", fg_color="#A1045A", hover_color="#E44982", font=("Arial Bold", 14), text_color="#ffffff", width=300)
submit_button.pack(anchor="w", pady=(40, 0), padx=(50, 0))
submit_button.configure(state="disabled")  

app.mainloop()
