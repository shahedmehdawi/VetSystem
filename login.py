import customtkinter as ct
import tkinter as ttk
from tkinter import messagebox
import PIL
import mysql.connector as msql


ct.set_appearance_mode("dark")  
ct.set_default_color_theme("green")

img = PIL.Image.open("./Assets/png-login.png")

class Login(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("500x450")
        
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
                                database='registration')# change database to match your database name
                mycursor=mydb.cursor()
                #messagebox.showerror("","Connected to database")
                command = "use registration"
                mycursor.execute(command)
                # we will execute a command to get username and password from table (login) ... you can call the table whatever you want too
                command="select * from login where username=%s and password=%s" # change table name to match your target table name
                mycursor.execute(command,(username,password)) #first and second %s will be replaced with username and password passed into mycursor.execute() 
                
                # fetches and returns a single query with the username and password we passed .... or returns None if not found
                myresult=mycursor.fetchone()
                if myresult != None:
                    messagebox.showerror("Success","Login Successful")
                    self.label2.configure(text="Login Successful")
                else:
                    messagebox.showerror("Failed","Login Failed")
                    self.label2.configure(text="Login Failed")
            except:
                messagebox.showerror("Failed","Couldn't connect to database")
            

app = Login()
app.mainloop()