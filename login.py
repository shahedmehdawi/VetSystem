import customtkinter as ct
import tkinter as ttk
from tkinter import messagebox
import PIL
import mysql.connector as msql
import bcrypt
from Crypto.Util.number import long_to_bytes


ct.set_appearance_mode("dark")  
ct.set_default_color_theme("green")

img = PIL.Image.open("./Assets/png-login.png") # change to match repo of image

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
            
    def login_check(self):
        username = self.username.get()
        password = self.password.get()
        if not(username) or not(password):
            self.label2.configure(text="please enter username and password")
            messagebox.showerror("Error", "Type Username and Password")
        else:
            try:
                #database credentials and information ... i named it registration .. you can name it whatever you want
                mydb=msql.connect(host="localhost", 
                                user='username',# change username to match your database user
                                password='password', # change pass
                                database='database_name')# change database to match your database name
                mycursor=mydb.cursor()
                #messagebox.showerror("","Connected to database")
                command = "use registration"
                mycursor.execute(command)
                # we will execute a command to get username, password_hash and salt from table (users) ... you can call the table whatever you want too
                command="select username, password_hash , salt from users where username=%s" # change table name to match your target table name
                mycursor.execute(command,(username,)) # %s will be replaced with username passed into mycursor.execute() 
                
                # fetches and returns a single query with the username and password we passed .... or returns None if not found
                myresult = mycursor.fetchone()
                if myresult == None:
                    messagebox.showerror("Failed","Login Failed")
                    self.label2.configure(text="Login Failed")
                else:
                    stored_pass_hash = myresult[1]
                    salt = myresult[2].decode()
                    
                    hashed_password = bcrypt.hashpw(password.encode(), salt.encode()).decode()
                    if hashed_password == stored_pass_hash:               
                        messagebox.showerror("Success","Login Successful")
                        self.label2.configure(text="Login Successful")
            except:
                messagebox.showerror("Failed","Couldn't connect to database")
            

app = Login()
app.mainloop()