import customtkinter as ct
from tkinter import messagebox
from PIL import Image
import mysql.connector as mysql
import bcrypt

HOST = "localhost"
USER = "root"  # change username
PASSWORD = "Bella*8234"  # change password
DATABASE = "new_schema"  # change database

class EditProfile(ct.CTk):
    def __init__(self, username):
        super().__init__()
        self.geometry("400x500")
        self.title("Vet Management System - Edit Profile")

        self.username = username

        self.edit_profile_frame = ct.CTkFrame(master=self, width=400, height=300)
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

    def load_user_info(self):
        try:
            mydb = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            cursor = mydb.cursor()
            command = "SELECT name, email FROM users WHERE username = %s"
            cursor.execute(command, (self.username,))
            user_info = cursor.fetchone()
            if user_info:
                name, email = user_info
                self.name_entry.insert(0, name)
                self.email_entry.insert(0, email)
            else:
                # User not found, proceed without displaying error message
                pass
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error retrieving user information: {err}")

    def save_changes(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        new_password = self.password_entry.get()

        try:
            mydb = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            cursor = mydb.cursor()

            if new_password:
                salt = bcrypt.gensalt(rounds=14)
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
                command = "UPDATE users SET name = %s, email = %s, password_hash = %s, salt = %s WHERE username = shahedmehdawi"
                cursor.execute(command, (name, email, hashed_password, salt, self.username))
            else:
                command = "UPDATE users SET name = %s, email = %s WHERE username = %s"
                cursor.execute(command, (name, email, self.username))

            mydb.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.destroy()
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error updating profile: {err}")

if __name__=="__main__":
    edit_profile_window = EditProfile("example_username")  # Replace "example_username" with actual username
    edit_profile_window.mainloop()
