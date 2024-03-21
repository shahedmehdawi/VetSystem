import customtkinter as ct
from tkinter import messagebox
from PIL import Image
import mysql.connector
import bcrypt

# Database connection details (replace with yours)
HOST = "localhost"
USER = "your_username"
PASSWORD = "your_password"
DATABASE = "your_database_name"

class Signup(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("Vet Management System - Signup")

        self.signup_frame = ct.CTkFrame(master=self, width=400, height=300)
        self.signup_frame.pack(pady=20)
        
        signup_username_label = ct.CTkLabel(master=self.signup_frame, text="Username:", font=("Roboto", 12))
        signup_username_label.pack(pady=10,padx=100)
        signup_username_entry = ct.CTkEntry(master=self.signup_frame, width=200)
        signup_username_entry.pack()

        signup_password_label = ct.CTkLabel(master=self.signup_frame, text="Password:", font=("Roboto", 12))
        signup_password_label.pack(pady=10)
        signup_password_entry = ct.CTkEntry(master=self.signup_frame, width=200, show="*")  # Hide password characters
        signup_password_entry.pack()

        signup_name_label = ct.CTkLabel(master=self.signup_frame, text="Name:", font=("Roboto", 12))
        signup_name_label.pack(pady=10)
        signup_name_entry = ct.CTkEntry(master=self.signup_frame, width=200)
        signup_name_entry.pack()

        signup_email_label = ct.CTkLabel(master=self.signup_frame, text="Email:", font=("Roboto", 12))
        signup_email_label.pack(pady=5)
        signup_email_entry = ct.CTkEntry(master=self.signup_frame, width=200)
        signup_email_entry.pack(pady=10)

        self.signup_button = ct.CTkButton(self, text="Sign Up", command=self.signup_user)
        self.signup_button.pack(pady=20)

        self.image = Image.open("Assets/cat_bg.png")
        self.bg_image = ct.CTkImage(light_image=self.image, dark_image=self.image,size=(400,500))
        self.bg_label = ct.CTkLabel(master=self,image=self.bg_image)
        self.bg_label.pack(fill="both")
        
        try:
            self.connect_db()
        except:
            pass
        
    def connect_db(self):
        try:
            global db, cursor
            db = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            cursor = db.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")

    def signup_user(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()

        salt = bcrypt.gensalt(rounds=10)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        sql = "INSERT INTO users (username, password_hash, name,) VALUES (%s, %s, ...)"
        val = (username, hashed_password, ...)
        try:
            cursor.execute(sql, val)
            db.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            # Clear signup form fields
        except mysql.connector.Error as err:
            messagebox.showerror("Signup Error", f"Error registering user: {err}")

# Create the signup window instance
signup_window = Signup()
signup_window.mainloop()