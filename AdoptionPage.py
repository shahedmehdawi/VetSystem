<<<<<<< HEAD
import mysql.connector
import tkinter
import customtkinter as ct
from PIL import ImageTk, Image
from tkinter import messagebox


class PetAdoption(ct.CTk):
    class DatabaseManager:
        def __init__(self):
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Bella*8234",
                database="new_schema"
            )
            self.cursor = self.db.cursor()

        def close_connection(self):
            self.cursor.close()
            self.db.close()

        def insert_customer(self, name, email, location, pet_name):
            query = "INSERT INTO customer (name, email, location, adopted_pet) VALUES (%s, %s, %s, %s)"
            values = (name, email, location, pet_name)
            self.cursor.execute(query, values)
            self.db.commit()    

    def __init__(self):
        super().__init__()
        self.title("Pet Adoption Page")
        self.geometry("1400x665")
        self.db_manager = self.DatabaseManager()
        self.setup_gui()

    def customer_details(self, pet_data):
        self.destroy()

    
        new_window = ct.CTk()  
        new_window.geometry("800x700")
        new_window.title('Adoption Details')

        
        new_window.configure() 

        
        title_label = ct.CTkLabel(new_window, text="🐾 Adoption Details 🐾", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
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
       
        name_label = ct.CTkLabel(new_window, text="Enter your Name:", font=("Arial", 12))
        name_label.pack()
        name_entry = ct.CTkEntry(new_window, font=("Arial", 12), width=300,corner_radius=50,fg_color=("lightpink"), text_color="black")
        name_entry.pack()

        
        email_label = ct.CTkLabel(new_window, text="Enter your Email:", font=("Arial", 12))
        email_label.pack()
        email_entry = ct.CTkEntry(new_window, font=("Arial", 12), width=300,corner_radius=50,fg_color=("lightpink"), text_color="black")
        email_entry.pack()

        
        location_label = ct.CTkLabel(new_window, text="Enter your Location:", font=("Arial", 12))
        location_label.pack()
        location_entry = ct.CTkEntry(new_window, font=("Arial", 12), width=300,corner_radius=50,fg_color=("lightpink"), text_color="black")
        location_entry.pack()

        submit_button = ct.CTkButton(new_window, text="Submit", font=("Arial", 12))
        submit_button.pack(pady=20)
        

        ##new_window.mainloop()

        def submit():
            name = name_entry.get()
            email = email_entry.get()
            location = location_entry.get()
            pet_name = pet_data[0]  # Get the pet name

            self.db_manager.insert_customer(name, email, location, pet_name)
            
            messagebox.showinfo("Adoption Success", f"You adopted {pet_name} successfully! 🐱 Now please wait for delivery.")
            new_window.destroy()  # Close the window after submission

        submit_button.configure(command=submit)

        new_window.mainloop()



    def setup_gui(self):
        title_label = ct.CTkLabel(self, text="Pets for Adoption <3", font=("Arial", 50))
        title_label.pack(pady=80)

        # /////// Fetch pet information including image path from the database
        cursor = self.db_manager.cursor
        cursor.execute("SELECT name, species, age, image_path FROM pets")
        pets_data = cursor.fetchall()

        for pet_data in pets_data:
            pet_frame = ct.CTkFrame(self)
            pet_frame.pack(side="left", padx=10)

            pet_label = ct.CTkLabel(pet_frame, text=pet_data[0], font=("Arial", 14))
            pet_label.pack()

            species_label = ct.CTkLabel(pet_frame, text=f"Species: {pet_data[1]}", font=("Arial", 12))
            species_label.pack()

            age_label = ct.CTkLabel(pet_frame, text=f"Age: {pet_data[2]}", font=("Arial", 12))
            age_label.pack()

            image = Image.open(pet_data[3])
            image = image.resize((260, 260))  
            photo = ImageTk.PhotoImage(image)
            image_label = ct.CTkLabel(pet_frame, image=photo)
            image_label.photo = photo
            image_label.pack()

            # ////// Bind a function to each image label to submit customer details when clicked
            image_label.bind("<Button-1>", lambda event, pet_data=pet_data: self.customer_details(pet_data))

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = PetAdoption()
    app.run()
=======
import mysql.connector
import tkinter
import customtkinter as ct
from PIL import ImageTk, Image
from tkinter import messagebox


class PetAdoption(ct.CTk):
    class DatabaseManager:
        def __init__(self):
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Bella*8234",
                database="new_schema"
            )
            self.cursor = self.db.cursor()

        def close_connection(self):
            self.cursor.close()
            self.db.close()

        def insert_customer(self, name, email, location, pet_name):
            query = "INSERT INTO customer (name, email, location, adopted_pet) VALUES (%s, %s, %s, %s)"
            values = (name, email, location, pet_name)
            self.cursor.execute(query, values)
            self.db.commit()    

    def __init__(self):
        super().__init__()
        self.title("Pet Adoption Page")
        self.geometry("1400x665")
        self.db_manager = self.DatabaseManager()
        self.setup_gui()

    def customer_details(self, pet_data):
        self.destroy()

    
        new_window = ct.CTk()  
        new_window.geometry("800x700")
        new_window.title('Adoption Details')

        
        new_window.configure() 

        
        title_label = ct.CTkLabel(new_window, text="🐾 Adoption Details 🐾", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
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
        

        ##new_window.mainloop()

        def submit():
            number = number_entry.get()
            location = location_entry.get()
            pet_name = pet_data[0]  # Get the pet name

            self.db_manager.insert_customer(number, location, pet_name)
            
            messagebox.showinfo("Adoption Success", f"You adopted {pet_name} successfully! 🐱 Now please wait for delivery.")
            new_window.destroy()  # Close the window after submission

        submit_button.configure(command=submit)

        new_window.mainloop()



    def setup_gui(self):
        title_label = ct.CTkLabel(self, text="Pets for Adoption <3", font=("Arial", 50))
        title_label.pack(pady=80)

        # /////// Fetch pet information including image path from the database
        cursor = self.db_manager.cursor
        cursor.execute("SELECT name, species, age, image_path FROM pets")
        pets_data = cursor.fetchall()

        for pet_data in pets_data:
            pet_frame = ct.CTkFrame(self)
            pet_frame.pack(side="left", padx=10)

            pet_label = ct.CTkLabel(pet_frame, text=pet_data[0], font=("Arial", 14))
            pet_label.pack()

            species_label = ct.CTkLabel(pet_frame, text=f"Species: {pet_data[1]}", font=("Arial", 12))
            species_label.pack()

            age_label = ct.CTkLabel(pet_frame, text=f"Age: {pet_data[2]}", font=("Arial", 12))
            age_label.pack()

            image = Image.open(pet_data[3])
            image = image.resize((260, 260))  
            photo = ImageTk.PhotoImage(image)
            image_label = ct.CTkLabel(pet_frame, image=photo)
            image_label.photo = photo
            image_label.pack()

            # ////// Bind a function to each image label to submit customer details when clicked
            image_label.bind("<Button-1>", lambda event, pet_data=pet_data: self.customer_details(pet_data))

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = PetAdoption()
    app.run()
>>>>>>> refs/remotes/origin/master
