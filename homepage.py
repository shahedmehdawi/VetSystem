import tkinter as tk
import customtkinter as ctk
import AdoptionPage
import editprofile
from PIL import Image
import login_linked_to_signup
from session_time_out import Session
import sys
sys.dont_write_bytecode = True

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

font1 = ("Helvetica", 14)

class Home(ctk.CTk):
    def __init__(self, username=None, role="normal_user"):  # Pass username as a parameter
        super().__init__()
        self.geometry("680x780")
        self.title("Homepage")
        self.username = username  # Store the username
        self.role = role

        title_label = ctk.CTkLabel(self, text=f"Welcome, {self.username} !", font=("Arial", 30))
        title_label.pack(pady=30, padx=10)

        self.frame = ctk.CTkFrame(self, height=500, width=300)
        self.frame.pack(pady=40, fill="both")

        self.my_image = ctk.CTkImage(dark_image=Image.open("Assets_Cat/homepage.png"), size=(600, 400))

        self.my_label = ctk.CTkLabel(self.frame, text='', image=self.my_image)
        self.my_label.pack(pady=20)

        self.button1 = ctk.CTkButton(self.frame, text="Pet Adoption", font=font1, command=self.move_to_adoption)
        self.button1.pack(pady=10, padx=10)

        self.button2 = ctk.CTkButton(self.frame, text="Edit profile", font=font1, command=self.move_to_edit)
        self.button2.pack(pady=10, padx=10)

        self.session_timeout = Session()
        self.after(0, self.check_session_timeout)  # Start checking session timeout after 100 milliseconds

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

    def move_to_adoption(self):
        if self.check_session_timeout()==True:
            self.destroy()
            login=login_linked_to_signup.Login()
            login.mainloop()
        else:
            self.destroy()
            adoption = AdoptionPage.PetAdoption(username=self.username, role=self.role)
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

##if __name__ == "__main__":
#    home = Home()
#    home.mainloop()