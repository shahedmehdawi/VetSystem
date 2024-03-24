import mysql.connector
import customtkinter as ct
from PIL import ImageTk, Image

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

    def __init__(self):
        super().__init__()
        self.title("Pet Adoption Page")
        self.geometry("1400x665")
        self.db_manager = self.DatabaseManager()
        self.setup_gui()

    def setup_gui(self):
        title_label = ct.CTkLabel(self, text="Pets for Adoption <3", font=("Arial", 50))
        title_label.pack(pady=80)

        # Fetch pet information including image paths from the database
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

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = PetAdoption()
    app.run()

