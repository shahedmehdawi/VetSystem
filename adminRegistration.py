from tkinter import ttk, messagebox
import mysql.connector as mysql
import bcrypt
from customtkinter import *
from PIL import Image
import uuid
import re
import login_linked_to_signup
from session_time_out import Session

import sys
sys.dont_write_bytecode = True

HOST = "localhost"
USER = "root"
PASSWORD = "QueueThatW@69"
DATABASE = "registration"

class App(CTk):
    def __init__(self, username, role):
        super().__init__()

        self.geometry("800x600")
        self.resizable(0, 0)
        self.username = username
        self.role = role
        side_img_data = Image.open("Assets_Cat/cybersecurity.jpg")
        password_icon_data = Image.open("Assets_Cat/password-icon.png")
        doctor_icon_data = Image.open("Assets_Cat/doctor.png")

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 600)) 
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(20, 20))
        doctor_icon = CTkImage(dark_image=doctor_icon_data, light_image=doctor_icon_data, size=(20, 20))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True, side="left")

        frame = CTkFrame(master=self, width=400, height=600, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome Admin", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 30)).pack(anchor="w", pady=(40, 10), padx=(50, 0))
        CTkLabel(master=frame, text=" Let's Register!", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(0,0), padx=(50, 0))

        CTkLabel(master=frame, text="  Username:", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 16), image=doctor_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(50, 0))
        self.username_entry = CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#A1045A", border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(50, 0))

        CTkLabel(master=frame, text="  Password:", text_color="#A1045A", anchor="w", justify="left", font=("Arial Bold", 16), image=password_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(50, 0))
        self.password_entry = CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#A1045A", border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(50, 0))

        label = CTkLabel(master=frame, text="Select Role:", text_color="#A1045A", font=("Arial Bold", 16))
        label.pack(anchor="w", pady=(30, 0), padx=(50, 0))

        options = ["Choose one", "doctor", "normal_user", "admin"]
        self.clicked = StringVar() 
        self.clicked.set("Choose one")

        style = ttk.Style()
        style.theme_use('clam')  

        style.configure('Custom.TMenubutton', foreground='#A1045A', font=('Arial Bold', 14), arrowcolor='#A1045A', relief='flat')

        drop = ttk.OptionMenu(frame, self.clicked, *options, style='Custom.TMenubutton')  
        drop.pack()

        back_button = CTkButton(self, text=" <--- back to Adoption page", font=("Arial", 13, "bold"), command=self.go_back)
        back_button.place(x=10, y=10)
        
        self.submit_button = CTkButton(master=frame, text="Submit", fg_color="#A1045A", hover_color="#E44982", font=("Arial Bold", 14), text_color="#ffffff", width=300, command=self.submit_registration)
        self.submit_button.pack(anchor="w", pady=(40, 0), padx=(50, 0))
        self.submit_button.configure(state="disabled")  

        # Add the trace callback after all widgets are initialized
        self.clicked.trace_add("write", self.enable_submit)  

        self.session_timeout=Session()
        self.after(0,self.check_session_timeout)

    def check_session_timeout(self):
        if self.session_timeout.has_timed_out():
            return True
        else:
            self.after(1000,self.check_session_timeout)

    def connect_db(self):
        try:
            mydb = mysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            return mydb
        except mysql.Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def go_back(self):
        if self.check_session_timeout()==True:
           self.destroy()
           login=login_linked_to_signup.Login()
           login.mainloop()
        else:
            self.destroy()  # Close the adoption page
            from AdminHomepage import AdminHome
            home_page = AdminHome(username=self.username, role=self.role)  # Open the home page
            home_page.mainloop()
    
    def register_user(self,username, password, role):
        mydb = self.connect_db()
        if mydb:
            cursor = mydb.cursor()
            try:
                # Hash the password before storing in the database
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                # Generate unique placeholders for name and email
                name = f"No name {uuid.uuid4()}"
                email = f"{uuid.uuid4()}@placeholder.com"
                is_new = True  # Default value for is_new
                # Insert user data into the 'users' table
                sql = "INSERT INTO users (username, name, email, password_hash, salt, role, is_new) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (username, name, email, hashed_password, salt, role, is_new)

                cursor.execute(sql, val)
                mydb.commit()
                print("User registered successfully!")
                messagebox.showinfo("Success", "User registered successfully!")
            except mysql.Error as err:
                print(f"Error registering user: {err}")
                messagebox.showerror("Error", f"Error registering user: {err}")
            finally:
                cursor.close()
                mydb.close()
                

    def validate_password(self, password):
        if len(password) < 12:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def enable_submit(self, *args):
        if hasattr(self, 'submit_button'):
            if self.clicked.get() != "Choose one":
                self.submit_button.configure(state="normal")
            else:
                self.submit_button.configure(state="disabled")

    def submit_registration(self):
        if self.check_session_timeout()==True:
           self.destroy()
           login=login_linked_to_signup.Login()
           login.mainloop()
        else:
            username = self.username_entry.get()
            password = self.password_entry.get()
            role = self.clicked.get()

            if not self.validate_password(password):
                messagebox.showerror("Invalid Password", "Password must be 12+ characters long and include uppercase, lowercase, numbers, and symbols.")
                return

            self.register_user(username, password, role)

#if __name__ == "__main__":
#     app = App()
#     app.mainloop()