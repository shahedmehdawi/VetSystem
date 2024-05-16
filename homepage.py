import tkinter as tk
import customtkinter as ctk
import AdoptionPage
import editprofile
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

font1=("Helvteica",14)

class Home(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("680x780")
        self.title("Homepage")

        title_label = ctk.CTkLabel(self, text="Welcome this is your Home Page :) ", font=("Arial", 30))
        title_label.pack(pady=30,padx=10)

        self.frame=ctk.CTkFrame(self,height=500,width=300)
        self.frame.pack(pady=40,fill="both")

        

        self.my_image=ctk.CTkImage(dark_image=Image.open("Assets_Cat/homepage.png"),size=(600,400))

        self.my_label=ctk.CTkLabel(self.frame,text='',image=self.my_image)
        self.my_label.pack(pady=20)


        self.button1=ctk.CTkButton(self.frame,text="Pet Adaption",font=font1,command=self.move_to_adoption)
        self.button1.pack(pady=10,padx=10)

        self.button2=ctk.CTkButton(self.frame,text="Edit profile",font=font1,command=self.move_to_edit)
        self.button2.pack(pady=10,padx=10)

    def move_to_adoption(self):
       self.destroy()
       adoption=AdoptionPage.PetAdoption() 
       adoption.mainloop()

    def move_to_edit(self):
        self.destroy()
        edit_page = editprofile.EditProfile()
        edit_page.mainloop()

home=Home()
home.mainloop()

