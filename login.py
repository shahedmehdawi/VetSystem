import customtkinter as ct
import tkinter as ttk
from tkinter import messagebox
import PIL
import mysql.connector as msql
import bcrypt
from Crypto.Util.number import long_to_bytes
from signup import Signup
from AdoptionPage import PetAdoption

ct.set_appearance_mode("dark")  
ct.set_default_color_theme("green")

img = PIL.Image.open("Assets/cat_bg.png") # change to match repo of image


def show_window(parent, width, height, title ,text): # I made this cuz tkinter messageboxes make the program trigger segmentation faults for some reason
    def close():
        window.destroy()
    window = ct.CTkToplevel(parent)
    window.title(f"{title}")
    window.geometry(f"{width}x{height}")
    window_label = ct.CTkLabel(window,text=f"{text}")
    window_label.pack(pady=5)
    new_button = ct.CTkButton(window, text="Ok", command=close)
    new_button.pack(pady=5)

class Login(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("600x450")
        
        self.frame1 = ct.CTkFrame(self, height=500, width=400)
        self.frame1.pack(pady=20)
        
        self.label1 = ct.CTkLabel(self.frame1, text="Login Page",
                        font=("Helvetica", 20))
        self.label1.pack(pady=20, padx=10)
        
        self.label2 = ct.CTkLabel(self, text="",
                        font=("Helvetica", 16))
        self.label2.pack(pady=20, padx=10)
        
        self.username = ct.CTkEntry(self.frame1, placeholder_text="enter username")
        self.username.pack(pady=10)
        
        self.password = ct.CTkEntry(self.frame1, placeholder_text="enter password", show="*")
        self.password.pack(pady=10)
        
        self.button1 = ct.CTkButton(self.frame1, text="login", command=self.login_check, image=ct.CTkImage(dark_image=img, light_image=img))
        self.button1.pack(pady=20, padx=120)

        self.signup_button = ct.CTkButton(self.frame1, text="Sign Up", command=self.go_to_signup)
        self.signup_button.pack(pady=10)

            
    def login_check(self):
        username = self.username.get()
        password = self.password.get()
        if not(username) or not(password):
            self.label2.configure(text="please enter username and password")
            #messagebox.showerror("Error", "Type Username and Password")
            show_window(self, 200,100, "error", "type username and password")
        else:
            try:
                #database credentials and information ... i named it registration .. you can name it whatever you want
                mydb=msql.connect(host="localhost", 
                                user='root',# change username to match your database user
                                password='QueueThatW@69', # change pass
                                database='registration')# change database to match your database name
                self.mycursor=mydb.cursor()
                #messagebox.showerror("","Connected to database")
                command = "use registration"
                self.mycursor.execute(command)
                # we will execute a command to get username, password_hash and salt from table (users) ... you can call the table whatever you want too
                command="select username, password_hash , salt from users where username=%s" # change table name to match your target table name
                self.mycursor.execute(command,(username,)) # %s will be replaced with username passed into mycursor.execute() 
                
                # fetches and returns a single query with the username and password we passed .... or returns None if not found
                myresult = self.mycursor.fetchone()
                if myresult == None:
                    # messagebox.showerror("Failed","Login Failed")
                    show_window(self, 200,100, "Failed", "Login Failed")
                    self.label2.configure(text="Login Failed")
                else:
                    stored_pass_hash = myresult[1]
                    salt = myresult[2].decode()
                    
                    hashed_password = bcrypt.hashpw(password.encode(), salt.encode()).decode()
                    if hashed_password == stored_pass_hash:               
                        #messagebox.showerror("Success","Login Successful")
                        show_window(self, 200,100, "Success", "Login Successful")
                        self.label2.configure(text="Login Successful")
                        self.go_to_Adoption()
            except:
                #messagebox.showerror("Failed","Couldn't connect to database")
                show_window(self, 200,100, "Failed","Couldn't connect to database")

                

    def go_to_signup(self): ## Function to transition to the sign-up page     
        self.destroy()             
        Signup_Window = Signup()
    
    def go_to_Adoption(self):
        self.destroy()
        adoption_page = PetAdoption()
        

if __name__ == "__main__":
    app = Login()
    app.mainloop()