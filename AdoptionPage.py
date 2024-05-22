import mysql.connector
import tkinter
import customtkinter as ct
from PIL import ImageTk, Image
from tkinter import messagebox
import re

import sys
sys.dont_write_bytecode = True

class PetAdoption(ct.CTk):
    class DatabaseManager:
        def __init__(self):
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="QueueThatW@69",
                database="registration"
            )
            self.cursor = self.db.cursor()

        def close_connection(self):
            self.cursor.close()
            self.db.close()

        def insert_customer(self, username, number, location, pet_name):
            # Retrieve customer's ID and name based on the username
            query = "SELECT UID, name FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            user_info = self.cursor.fetchone()
            if user_info:
                user_id, name = user_info
            # Insert customer information into the customer_info table
                query = "INSERT INTO customer_info (id, name, number, location, pet_info) VALUES (%s, %s, %s, %s, %s)"
                values = (user_id, name, number, location, pet_name)
                self.cursor.execute(query, values)
                self.db.commit()
            else:
                # Handle case where user is not found
                messagebox.showerror("Error", "User not found")


    def __init__(self, username=None, role="admin"):
        super().__init__()
        self.title("Pet Adoption Page")
        self.geometry("1400x665")
        self.username = username
        self.role = role
        self.db_manager = self.DatabaseManager()
        self.setup_gui()

    def validate_phone_number(self, phone_number):
    # Regular expression pattern for phone number validation
        pattern = r'^07[789]\d{7}$'
        if re.match(pattern, phone_number):
            return True  # Valid phone number
        else:
            return False  # Invalid phone number 
    
    def customer_details(self, pet_data):
        if pet_data[5] == 1:
            messagebox.showinfo(title="hmmm", message="Pet is adopted, choose another one")
        else:
            
            # Function to handle back button click event
            def go_back():
                new_window.destroy()
                #self.deiconify() ##The window remains alive in memory and can be made visible again using deiconify()
                from homepage import Home
                home_page = Home(username=self.username, role=self.role)  # Open the home page
                home_page.mainloop()
            
            def go_back_admin():
                new_window.destroy()
                #self.deiconify() ##The window remains alive in memory and can be made visible again using deiconify()
                from AdminHomepage import AdminHome
                home_page = AdminHome(username=self.username, role=self.role) 
                home_page.mainloop()
            
            def pet_adopted():
                cursor = self.db_manager.cursor
                cursor.execute("SELECT UID FROM users WHERE username = %s", (self.username,))
                result = cursor.fetchone()

                if result:
                    customer_uid = result[0]

                    pet_id = int(pet_data[4])  # Ensure pet_id is an integer
                    cursor.execute("UPDATE `pets` SET `adopted` = 1, `customer_id` = %s WHERE `id` = %s;", (customer_uid, pet_id))
                    self.db_manager.db.commit()  # Commit the changes
                else:
                    messagebox.showerror("Error", "User not found")
            
            def submit():
                number = number_entry.get()
                location = location_entry.get()
                pet_name = pet_data[0]  # Get the pet name
                pet_id = pet_data[4]

                try:
                    if self.validate_phone_number(number):
                        # If phone number is valid, proceed with insertion
                        self.db_manager.insert_customer(self.username, number, location, pet_name)
                        pet_adopted()
                        messagebox.showinfo("Adoption Success", f"You adopted {pet_name} successfully! 🐱 Now please wait for delivery.")
                        #new_window.destroy()  # Close the window after submission
                        if self.role != "admin":
                            go_back()
                        else:
                            go_back_admin()
                    else:
                        # If phone number is invalid, display error message
                        messagebox.showerror("error", "Invalid phone number ! please make sure that you provide us with a valid phone number")
                except:
                    pet_adopted()
                    messagebox.showinfo("Adoption Success", f"You adopted {pet_name} successfully! 🐱 Now please wait for delivery.")
                    if self.role != "admin":
                            go_back()
                    else:
                        go_back_admin()
            self.destroy()

        
            new_window = ct.CTk()  
            new_window.geometry("800x700")
            new_window.title('Adoption Details')

            
            new_window.configure() 

            
            title_label = ct.CTkLabel(new_window, text="🐾 Adoption Details 🐾", font=("Arial", 24, "bold"))
            title_label.pack(pady=20)

            # Add a back button to the top left corner
            back_button = ct.CTkButton(new_window, text=" <--- back to Adoption page" if self.role != "admin" else " <--- back to Admin Adoption page", font=("Arial", 13, "bold"), command=go_back if self.role != "admin" else go_back_admin)
            back_button.place(x=10, y=10)
            
            sub_title = ct.CTkLabel(new_window, text="pet you picked: ", font=("Arial", 18, "bold"), text_color="lightpink")
            sub_title.pack(pady=30)
            
            pet_name_label = ct.CTkLabel(new_window, text=f"Name: {pet_data[0]}", font=("Arial", 12))
            pet_name_label.pack()
            species_label = ct.CTkLabel(new_window, text=f"Species: {pet_data[1]}", font=("Arial", 12))
            species_label.pack()
            age_label = ct.CTkLabel(new_window, text=f"Age: {pet_data[2]}", font=("Arial", 12))
            age_label.pack()
            sub_title2 = ct.CTkLabel(new_window, text="to confirm your order ฅ^•ﻌ•^ฅ: ", font=("Arial", 18, "bold"), text_color="lightpink")
            sub_title2.pack(pady=50)
            
            number_label = ct.CTkLabel(new_window, text="Enter your Number:", font=("Arial", 12))
            number_label.pack()
            number_entry = ct.CTkEntry(new_window, font=("Arial", 12), width=300,corner_radius=50,fg_color=("lightpink"), text_color="black")
            number_entry.pack()

            
            location_label = ct.CTkLabel(new_window, text="Enter your Location:", font=("Arial", 12))
            location_label.pack()
            location_entry = ct.CTkEntry(new_window, font=("Arial", 12), width=300,corner_radius=50,fg_color=("lightpink"), text_color="black")
            location_entry.pack()


            submit_button = ct.CTkButton(new_window, text="Submit", font=("Arial", 12))
            submit_button.pack(pady=20)
            
            submit_button.configure(command=submit)

            new_window.mainloop()
            

            ##new_window.mainloop()



    def setup_gui(self):
        title_label = ct.CTkLabel(self, text="Pets for Adoption <3", font=("Arial", 50))
        title_label.pack(pady=80)

        scrollable_frame = ct.CTkScrollableFrame(self, orientation="horizontal", width=1300, height=800)
        scrollable_frame.pack(pady=10)
        # /////// Fetch pet information including image path from the database
        cursor = self.db_manager.cursor
        cursor.execute("SELECT name, species, age, image_path, id, adopted FROM pets")
        pets_data = cursor.fetchall()

        for pet_data in pets_data:
            pet_frame = ct.CTkFrame(scrollable_frame)
            pet_frame.pack(side="left", padx=10)

            pet_label = ct.CTkLabel(pet_frame, text=pet_data[0], font=("Arial", 14))
            pet_label.pack()

            species_label = ct.CTkLabel(pet_frame, text=f"Species: {pet_data[1]}", font=("Arial", 12))
            species_label.pack()

            age_label = ct.CTkLabel(pet_frame, text=f"Age: {pet_data[2]}", font=("Arial", 12))
            age_label.pack()

            adopted_label = ct.CTkLabel(pet_frame, text=f"pet is adopted" if pet_data[5]==1 else "pet is available for adoption", font=("Arial", 12), text_color="red" if pet_data[5]==1 else "white")
            adopted_label.pack()
            
            # id_label = ct.CTkLabel(pet_frame, text=f"ID = {pet_data[4]}", font=("Arial", 12))
            # id_label.pack()
            
            image = Image.open(pet_data[3])
            image = image.resize((260, 260))  
            photo = ImageTk.PhotoImage(image)
            image_label = ct.CTkLabel(pet_frame, image=photo)
            image_label.photo = photo
            image_label.pack()

            # ////// Bind a function to each image label to submit customer details when clicked
            image_label.bind("<Button-1>", lambda event, pet_data=pet_data: self.customer_details(pet_data))

            back_button = ct.CTkButton(self, text="<--- Back to Home" if self.role != "admin" else "Back to AdminHome", font=("Arial", 13, "bold"), command=self.go_back if self.role != "admin" else self.redirect_to_Adminhome)
            back_button.place(x=10, y=10)
    
    def go_back(self):
        self.destroy()  # Close the adoption page
        from homepage import Home
        home_page = Home(username=self.username, role=self.role)  # Open the home page
        home_page.mainloop()
    
    def redirect_to_Adminhome(self):
        # Destroy current window and create Home instance
        self.destroy()
        from AdminHomepage import AdminHome
        home_page = AdminHome(username=self.username, role=self.role) 
        home_page.mainloop()
    
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = PetAdoption()
    app.run()