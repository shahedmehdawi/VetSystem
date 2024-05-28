import re
import mysql.connector as mysql
import bcrypt
import customtkinter as ct
from tkinter import messagebox
import login_linked_to_signup
from session_time_out import Session
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

import sys
sys.dont_write_bytecode = True

HOST = "localhost"
USER = "root"  # change username
PASSWORD = "QueueThatW@69"  # change password
DATABASE = "registration"  # change database

class NewProfile(ct.CTk):
    def __init__(self, username, role, stored_pass_hash, salt):
        super().__init__()
        self.geometry("600x500")
        self.title("Vet Management System - Edit Profile")

        self.username = username
        self.role = role
        self.stored_pass_hash = stored_pass_hash
        self.salt = salt
        
        self.edit_profile_frame = ct.CTkFrame(master=self, width=550, height=400)
        self.edit_profile_frame.pack(pady=20)

        self.name_label = ct.CTkLabel(master=self.edit_profile_frame, text="Name:", font=("Roboto", 12))
        self.name_label.pack(pady=10)
        self.name_entry = ct.CTkEntry(master=self.edit_profile_frame, width=200)
        self.name_entry.pack()

        self.email_label = ct.CTkLabel(master=self.edit_profile_frame, text="Email:", font=("Roboto", 12))
        self.email_label.pack(pady=5)
        self.email_entry = ct.CTkEntry(master=self.edit_profile_frame, width=200)
        self.email_entry.pack(pady=10)

        self.password_label = ct.CTkLabel(master=self.edit_profile_frame, text="New Password:", font=("Roboto", 12))
        self.password_label.pack(pady=10)
        self.password_entry = ct.CTkEntry(master=self.edit_profile_frame, width=200, show="*")  # Hide password characters
        self.password_entry.pack()

        self.save_button = ct.CTkButton(self, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=20)

        self.load_user_info()

        self.session_timeout = Session()
        self.after(0, self.check_session_timeout)

    def check_session_timeout(self):
        if self.session_timeout.has_timed_out():
            return True
        else:
            self.after(1000, self.check_session_timeout)

    def redirect_to_Login(self):
        # Destroy current window and create Home instance
        self.destroy()
        from login_linked_to_signup import Login
        Login_page = Login() 
        Login_page.mainloop()

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

    def validate_email(self, email):
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return email_pattern.match(email) is not None

    def get_or_create_key(self, cursor, mydb):
        cursor.execute("SELECT enc_key FROM encryption_keys WHERE id = 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            key = os.urandom(32)  # AES key size is 32 bytes for AES-256
            cursor.execute("INSERT INTO encryption_keys (id, enc_key) VALUES (1, %s)", (key,))
            mydb.commit()
            return key

    def encrypt_name(self, name, cursor, mydb):
        key = self.get_or_create_key(cursor, mydb)
        iv = os.urandom(16)  # AES block size is 16 bytes
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(name.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode(), iv

    def load_user_info(self):
        try:
            mydb = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            cursor = mydb.cursor()
            command = "SELECT email FROM users WHERE username = %s"
            cursor.execute(command, (self.username,))
            user_info = cursor.fetchone()
            if user_info:
                email = user_info[0]
                self.email_entry.insert(0, email)
            else:
                # User not found, proceed without displaying error message
                pass
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error retrieving user information: {err}")

    def save_changes(self):
        if self.check_session_timeout() == True:
            self.destroy()
            login = login_linked_to_signup.Login()
            login.mainloop()
        else:
            name = self.name_entry.get()
            email = self.email_entry.get()
            new_password = self.password_entry.get()
            hashed_password = bcrypt.hashpw(new_password.encode(), self.salt.encode()).decode()

            if self.stored_pass_hash == hashed_password:
                messagebox.showerror("Invalid Password", "Password cannot match old password")
                return
            

            try:
                mydb = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
                cursor = mydb.cursor()
                encrypted_name, iv = self.encrypt_name(name, cursor, mydb)


                if not name:
                    messagebox.showerror("Invalid Name", "Please Enter a valid Name")
                    return
                elif not self.validate_password(new_password):
                    messagebox.showerror("Invalid Password", "Password must be 12+ characters long and include uppercase, lowercase, numbers, and symbols.")
                    return
                elif not self.validate_email(email):
                    messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                    return
                else:
                    salt = bcrypt.gensalt(rounds=14)
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
                    command = "UPDATE users SET name = %s, email = %s, password_hash = %s, salt = %s,iv=%s, is_new = 0 WHERE username = %s "
                    cursor.execute(command, (encrypted_name, email, hashed_password, salt,iv ,self.username))
                    mydb.commit()
                    messagebox.showinfo("Success", "Profile updated successfully!")
                    self.redirect_to_Login()
                ##self.destroy()
            except mysql.Error as err:
                messagebox.showerror("Database Error", f"Error updating profile: {err}")
                