import tkinter
import mysql.connector
from tkinter import messagebox
from datetime import datetime
import customtkinter as ct

class AppointmentBooking(ct.CTk):
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bella*8234",
            database="new_schema"
        )
        self.cursor = self.db.cursor()

        self.root = ct.CTk()
        self.root.title("Veterinary Clinic Appointment Booking")

        self.setup_gui()

    def book_appointment(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        pet_type = self.pet_type_var.get()
        date = self.date_entry.get()
        reason = self.reason_entry.get()

        if name and email and pet_type and date and reason:
            self.cursor.execute("INSERT INTO appointment (name, email, pet_type, date, reason) VALUES (%s, %s, %s, %s, %s)",
                               (name, email, pet_type, date, reason))
            self.db.commit()
            messagebox.showerror("Success", "Appointment booked successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def setup_gui(self):
        ct.CTkLabel(self.root, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = ct.CTkEntry(self.root)
        self.name_entry.grid(row=0, column=1)

        ct.CTkLabel(self.root, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = ct.CTkEntry(self.root)
        self.email_entry.grid(row=1, column=1)

        pet_types = ["Cat", "Dog", "Hamster", "Rabbit", "Bird"]
        ct.CTkLabel(self.root, text="Pet Type:").grid(row=2, column=0, sticky="w")
        self.pet_type_var = ct.StringVar(self.root)
        self.pet_type_var.set(pet_types[0])  # Default pet type
        pet_type_menu = ct.CTkOptionMenu(self.root, self.pet_type_var.get(), *pet_types)
        pet_type_menu.grid(row=2, column=1)

        ct.CTkLabel(self.root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.date_entry = ct.CTkEntry(self.root)
        self.date_entry.grid(row=3, column=1)

        ct.CTkLabel(self.root, text="Reason:").grid(row=4, column=0, sticky="w")
        self.reason_entry = ct.CTkEntry(self.root)
        self.reason_entry.grid(row=4, column=1)

        book_button = ct.CTkButton(self.root, text="Book Appointment", command=self.book_appointment)
        book_button.grid(row=5, columnspan=2)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppointmentBooking()
    app.run()
