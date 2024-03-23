import customtkinter as ct
from tkinter import messagebox
from PIL import Image
import mysql.connector as mysql
import bcrypt
from CTkMessagebox import CTkMessagebox

HOST = "localhost"
USER = "root" # change username
PASSWORD = "QueueThatW@69" # change password
DATABASE = "registration" # change database

class Signup(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("480x800")
        self.resizable(False,False)
        self.title("Vet Management System - Signup")

        self.signup_frame = ct.CTkFrame(master=self, width=400, height=300)
        self.signup_frame.pack(pady=20)
        
        self.image = Image.open("Assets/cat_bg.png")
        self.bg_image = ct.CTkImage(light_image=self.image, dark_image=self.image,size=(450,530))
        self.bg_label = ct.CTkLabel(master=self,image=self.bg_image, text="")
        self.bg_label.place(x=10,y=350)
        
        self.signup_username_label = ct.CTkLabel(master=self.signup_frame, text="Username:", font=("Roboto", 12))
        self.signup_username_label.pack(pady=10,padx=100)
        self.signup_username_entry = ct.CTkEntry(master=self.signup_frame, width=200)
        self.signup_username_entry.pack()

        self.signup_password_label = ct.CTkLabel(master=self.signup_frame, text="Password:", font=("Roboto", 12))
        self.signup_password_label.pack(pady=10)
        self.signup_password_entry = ct.CTkEntry(master=self.signup_frame, width=200, show="*")  # Hide password characters
        self.signup_password_entry.pack()

        self.signup_name_label = ct.CTkLabel(master=self.signup_frame, text="Name:", font=("Roboto", 12))
        self.signup_name_label.pack(pady=10)
        self.signup_name_entry = ct.CTkEntry(master=self.signup_frame, width=200)
        self.signup_name_entry.pack()

        self.signup_email_label = ct.CTkLabel(master=self.signup_frame, text="Email:", font=("Roboto", 12))
        self.signup_email_label.pack(pady=5)
        self.signup_email_entry = ct.CTkEntry(master=self.signup_frame, width=200)
        self.signup_email_entry.pack(pady=10)

        self.signup_button = ct.CTkButton(self, text="Sign Up", command=self.signup_user)
        self.signup_button.pack(pady=20)

        
        
    def connect_db(self):
        try:
            global mydb, cursor
            mydb=mysql.connect(host="localhost", 
                                user="root",
                                password="QueueThatW@69",
                                database="registration")
            cursor = mydb.cursor()
            command = "use registration"
            cursor.execute(command)
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")

    def signup_user(self):
        self.connect_db()
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()
        
        if not(username) or not(password) or not(name) or not(email):
            def close():
                error_window.destroy()
                error_window.update()
            error_window = ct.CTkToplevel(self)
            error_window.title("error registering user")
            error_window.geometry("280x130")
            textincomplete = ct.CTkLabel(error_window,text="Fill all fields please")
            textincomplete.pack(pady=5)
            new_button = ct.CTkButton(error_window, text="Ok", command=close)
            new_button.pack(pady=20)
        else:
            salt = bcrypt.gensalt(rounds=14)
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            sql = "INSERT INTO users (username, password_hash, name, email, salt) VALUES (%s, %s, %s, %s, %s)"
            val = ( username, hashed_password, name, email, salt)
            try:
                def open_login():
                    success_window.destroy()
                    success_window.update()
                    self.destroy()
                    from login import Login
                    Login_Page = Login()
                
                
                cursor.execute(sql, val)
                mydb.commit()
                success_window = ct.CTkToplevel(self, fg_color="grey")
                success_window.title("Registration Successful")
                success_window.geometry("250x100")
                
                new_button = ct.CTkButton(success_window, text="Ok", command=open_login)
                new_button.pack(pady=20)
                
            except mysql.Error as err:
                def close():
                    error_window.destroy()
                    error_window.update()
                error_window = ct.CTkToplevel(self)
                error_window.title("error registering user")
                error_window.geometry("280x130")
                
                if "username" in str(err):
                    text1 = ct.CTkLabel(error_window,text="Duplicate username ,\nplease enter a different username")
                elif "email" in str(err):
                    text1 = ct.CTkLabel(error_window,text="Duplicate email ,\nplease enter a different email")
                text1.pack(pady=5)
                new_button = ct.CTkButton(error_window, text="Ok", command=close)
                new_button.pack(pady=20)

if __name__ == "__main__":
    signup_window = Signup()
    signup_window.mainloop()