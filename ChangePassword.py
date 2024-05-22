import customtkinter as ct
from tkinter import messagebox
from PIL import Image
import mysql.connector as mysql
import bcrypt

import sys
sys.dont_write_bytecode = True

HOST = "localhost"
USER = "root" # change username
PASSWORD = "QueueThatW@69" # change password
DATABASE = "registration" # change database

class changePass(ct.CTk):
    def __init__(self, username):
        super().__init__()
        self.geometry("490x400")
        self.title("Vet Management System - Change Password")

        ##self.username = username

        # Frame for change pass
        self.changePass_frame = ct.CTkFrame(master=self, width=380, height=280, corner_radius=15)
        self.changePass_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Title Label
        self.title_label = ct.CTkLabel(master=self.changePass_frame, text="Change your Password first !", font=("Roboto", 18, "bold"))
        self.title_label.pack(pady=20)

        # New Password Label and Entry
        self.password_label = ct.CTkLabel(master=self.changePass_frame, text="New Password:", font=("Roboto", 12))
        self.password_label.pack(pady=10)
        self.password_entry = ct.CTkEntry(master=self.changePass_frame, width=200, show="*")
        self.password_entry.pack()

        # Confirm Password Label and Entry
        self.confirm_password_label = ct.CTkLabel(master=self.changePass_frame, text="Confirm Password:", font=("Roboto", 12))
        self.confirm_password_label.pack(pady=10)
        self.confirm_password_entry = ct.CTkEntry(master=self.changePass_frame, width=200, show="*")
        self.confirm_password_entry.pack()

        # Save Changes Button
        self.save_button = ct.CTkButton(self.changePass_frame, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=20)

    def save_changes(self):
        new_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not new_password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        try:
            mydb = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            cursor = mydb.cursor()

            salt = bcrypt.gensalt(rounds=14)
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            command = "UPDATE users SET password_hash = %s, salt = %s WHERE username = %s"
            cursor.execute(command, (hashed_password, salt, self.username))

            mydb.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            self.destroy()
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error updating password: {err}")


changePass('shahed').mainloop()