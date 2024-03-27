import customtkinter as ct
from tkinter import messagebox
from PIL import Image
import mysql.connector as mysql
import bcrypt


HOST = "localhost"
USER = "root" # change username
PASSWORD = "Bella*8234" # change password
DATABASE = "new_schema" # change database

class Signup(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("Vet Management System - Signup")

        self.signup_frame = ct.CTkFrame(master=self, width=400, height=300)
        self.signup_frame.pack(pady=20)
        
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

        self.image = Image.open("Assets/cat_bg.png")
        self.bg_image = ct.CTkImage(light_image=self.image, dark_image=self.image,size=(400,500))
        self.bg_label = ct.CTkLabel(master=self,image=self.bg_image)
        self.bg_label.pack(fill="both")
        
        self.connect_db()
        
    def connect_db(self):
        try:
            global mydb, cursor
            mydb=mysql.connect(host=HOST, 
                                user=USER,
                                password=PASSWORD,
                                database=DATABASE)
            cursor = mydb.cursor()
            command = "use new_schema"
            cursor.execute(command)
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")

    def signup_user(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()

        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        sql = "INSERT INTO users (username, password_hash, name, email, salt) VALUES (%s, %s, %s, %s, %s)"
        val = (username, hashed_password, name, email, salt)
        try:
            cursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Success", "User registered successfully!")

        except mysql.Error as err:
            messagebox.showerror("Signup Error", f"Error registering user: {err}")


signup_window = Signup()
signup_window.mainloop()