import tkinter as tk
import customtkinter as ctk
import AdoptionPage
import adminRegistration
import editprofile
from PIL import Image
import login_linked_to_signup
from session_time_out import Session

import sys
sys.dont_write_bytecode = True

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

font1=("Helvteica",14)


class AdminHome(ctk.CTk):
    def __init__(self,username=None, role="admin"):  # Pass username as a parameter
        super().__init__()
        self.geometry("680x780")
        self.title("Homepage")
        self.username = username  # Store the username
        self.role = role


        title_label = ctk.CTkLabel(self, text=f"Welcome, {self.username} !", font=("Arial", 30))
        title_label.pack(pady=30,padx=10)

        self.frame=ctk.CTkFrame(self,height=500,width=300)
        self.frame.pack(pady=40,fill="both")

        

        self.my_image=ctk.CTkImage(dark_image=Image.open("Assets_Cat/homepage.png"),size=(600,400))

        self.my_label=ctk.CTkLabel(self.frame,text='',image=self.my_image)
        self.my_label.pack(pady=20)


        self.button1=ctk.CTkButton(self.frame,text="Pet Adoption",font=font1,command=self.move_to_adoption)
        self.button1.pack(pady=10,padx=10)

        self.button2=ctk.CTkButton(self.frame,text="Edit profile",font=font1,command=self.move_to_edit)
        self.button2.pack(pady=10,padx=10)
        
        self.button3=ctk.CTkButton(self.frame,text="Admin Panel",font=font1,command=self.move_to_AdminPanel)
        self.button3.pack(pady=10,padx=10)

        self.session_timeout=Session()
        self.after(0,self.check_session_timeout)

    def check_session_timeout(self):
        if self.session_timeout.has_timed_out():
            return True
        else:
            self.after(1000,self.check_session_timeout)

    def move_to_adoption(self):
       if self.check_session_timeout()==True:
           self.destroy()
           login=login_linked_to_signup.Login()
           login.mainloop()
       else:
        self.destroy()
        adoption=AdoptionPage.PetAdoption(username=self.username, role =self.role) 
        adoption.mainloop()

    def move_to_edit(self):
        if self.check_session_timeout()==True:
           self.destroy()
           login=login_linked_to_signup.Login()
           login.mainloop()
        else:
            self.destroy()
            edit_page = editprofile.EditProfile(username=self.username,role=self.role)
            edit_page.mainloop()
        
    def move_to_AdminPanel(self):
       if self.check_session_timeout()==True:
           self.destroy()
           login=login_linked_to_signup.Login()
           login.mainloop()
       else: 
           self.destroy()
           AdminPage=adminRegistration.App(username=self.username, role=self.role) 
           AdminPage.mainloop()

#home=AdminHome()
#home.mainloop()

