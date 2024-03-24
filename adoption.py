import customtkinter as ct
from PIL import ImageTk, Image

class PetAdoptionPage(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x600")
        self.title("Pet Adoption Page")

        self.pets = [
            {"name": "Bella", "species": "Cat", "age": "3 years", "image": "cat.jpg"},
            {"name": "Max", "species": "Dog", "age": "2 years", "image": "dog.jpg"},
            {"name": "Charlie", "species": "Rabbit", "age": "1 year", "image": "rabbit.jpg"},
            {"name": "Snowball", "species": "Hamster", "age": "6 months", "image": "hamster.jpg"},
            {"name": "Kiwi", "species": "Bird", "age": "1 year", "image": "bird.jpg"}
        ]

        self.setup_gui()

    def setup_gui(self):
        ct.CTkLabel(self, text="Available Pets", font=("Arial", 16)).pack()

        for pet in self.pets:
            pet_frame = ct.CTkFrame(self)
            pet_frame.pack(side="left", padx=10)  # Pack frames horizontally with padding

            pet_label = ct.CTkLabel(pet_frame, text=pet["name"], font=("Arial", 14))
            pet_label.pack()

            species_label = ct.CTkLabel(pet_frame, text=f"Species: {pet['species']}", font=("Arial", 12))
            species_label.pack()

            age_label = ct.CTkLabel(pet_frame, text=f"Age: {pet['age']}", font=("Arial", 12))
            age_label.pack()

            image = Image.open(pet["image"])
            image = image.resize((150, 150))  # Resize image
            photo = ImageTk.PhotoImage(image)
            image_label = ct.CTkLabel(pet_frame, image=photo)
            image_label.photo = photo  # Keep a reference to the photo
            image_label.pack()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = PetAdoptionPage()
    app.run()

