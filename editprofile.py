import re
import mysql.connector as mysql
import bcrypt
import customtkinter as ct
from tkinter import messagebox
import login_linked_to_signup
from session_time_out import Session
import base64
import sys
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


HOST = "localhost"
USER = "root"  # change username
PASSWORD = "Bella*8234"  # change password
DATABASE = "new_schema"  # change database

class EditProfile(ct.CTk):
    def __init__(self, username,role="admin"):
        super().__init__()
        self.geometry("600x500")
        self.title("Vet Management System - Edit Profile")

        self.username = username
        self.role=role
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

        back_button = ct.CTkButton(self, text="<--- Back to Home" if self.role != "admin" else "Back to AdminHome", font=("Arial", 13, "bold"), command=self.go_back if self.role != "admin" else self.redirect_to_Adminhome)        
        back_button.place(x=10, y=10)

        self.session_timeout = Session()
        self.after(0, self.check_session_timeout)

    def check_session_timeout(self):
        current_time=self.session_timeout.read_from_db()
        time_difference = (current_time - self.session_timeout.start_time).total_seconds()
        print("current_time= ",current_time)    
        print("start_time= ",self.session_timeout.start_time)
        print("difference_time= ",time_difference)
        if self.session_timeout.has_timed_out():
            return True
        else:
            self.after(1000, self.check_session_timeout)  # Check again after 1 second   

    def redirect_to_Adminhome(self):
        if self.check_session_timeout()==True:
            self.destroy()
            login=login_linked_to_signup.Login()
            login.mainloop()
        else:
            self.destroy()
            from AdminHomepage import AdminHome
            home_page = AdminHome(username=self.username, role=self.role) 
            home_page.mainloop()

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

    def go_back(self):
        self.destroy()  # Close the adoption page
        from homepage import Home
        home_page = Home(username=self.username)  # Open the home page
        home_page.mainloop()

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

            try:
                mydb = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
                cursor = mydb.cursor()
                encrypted_name, iv = self.encrypt_name(name, cursor, mydb)
                
                if not name:
                    messagebox.showerror("Invalid Name", "Please Enter a valid Name")
                    return
                elif not self.validate_email(email):
                    messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                    return

                if new_password:
                    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$%*?&])[A-Za-z\d@$%*?&]{10,}$', new_password):
                        salt = bcrypt.gensalt(rounds=14)
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
                        command = "UPDATE users SET name = %s, email = %s, password_hash = %s, salt = %s, iv= %s WHERE username = %s "
                        cursor.execute(command, (encrypted_name, email, hashed_password, salt,iv, self.username))
                    else:
                        messagebox.showerror("Password Error", "Password must be at least 10 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one of the following symbols: @, $, %, *, ?, &")
                        return
                else:
                    command = "UPDATE users SET name = %s, email = %s, iv=%s WHERE username = %s"
                    cursor.execute(command, (encrypted_name, email,iv, self.username))

                mydb.commit()
                messagebox.showinfo("Success", "Profile updated successfully!")
                ##self.destroy()
            except mysql.Error as err:
                messagebox.showerror("Database Error", f"Error updating profile: {err}")
