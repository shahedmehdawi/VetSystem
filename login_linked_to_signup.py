import customtkinter as ct
import tkinter as ttk
from tkinter import messagebox
import PIL
import mysql.connector as msql
import bcrypt
from Crypto.Util.number import long_to_bytes
import editprofile

import sys
sys.dont_write_bytecode = True

ct.set_appearance_mode("dark")
ct.set_default_color_theme("green")

img = PIL.Image.open("Assets_Cat/c.jpg") # change to match repo of image
buttonClicked = False # Bfore first click

class Login(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("600x500")
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
            messagebox.showerror("Error", "Type Username and Password")
        else:
            try:
                #database credentials and information ... i named it new_schema .. you can name it whatever you want
                mydb=msql.connect(host="localhost", 
                                user='root',# change username to match your database user
                                password='QueueThatW@69', # change pass
                                database='registration')# change database to match your database name
                mycursor=mydb.cursor()
                #messagebox.showerror("","Connected to database")
                command = "use registration"
                mycursor.execute(command)
                # we will execute a command to get username, password_hash and salt from table (users) ... you can call the table whatever you want too
                command="select UID, username, password_hash , salt, role, is_new from users where username=%s" # change table name to match your target table name
                mycursor.execute(command,(username,)) # %s will be replaced with username passed into mycursor.execute() 

                # fetches and returns a single query with the username and password we passed .... or returns None if not found
                myresult = mycursor.fetchone()
                if myresult == None:
                    self.login_logs(mydb,mycursor,None,username,"Failed Login")
                    messagebox.showerror("Failed","Login Failed")
                    self.label2.configure(text="Login Failed")
                else: 
                    stored_pass_hash = myresult[2]
                    salt = myresult[3].decode()
                    role = myresult[4]
                    is_new = myresult[5]
                    user_id=myresult[0]
                    hashed_password = bcrypt.hashpw(password.encode(), salt.encode()).decode()
                    if hashed_password == stored_pass_hash: 
                        if is_new:
                            self.redirect_to_EditProfile(username, role, stored_pass_hash, salt)
                            return
                        #to insert logs in user_logs table
                        self.login_logs(mydb,mycursor,user_id,username,"Successful Login")
                        #messagebox.showerror("Success","Login Successful")
                        self.label2.configure(text="Login Successful")
                        # Redirect to home page
                        if role != "admin":
                            self.redirect_to_home(username, role)
                        else:
                            self.redirect_to_Adminhome(username, role)
                    else:
                        self.login_logs(mydb,mycursor,user_id,username,"Failed Login")
                        messagebox.showerror("Login Failed","invalid username or password")
            except:
                messagebox.showerror("Failed","Couldn't connect to database")

    def login_logs(self,mydb,mycursor,user_id,username,action):
        try:    
            command="insert into login_logs(user_id,username,action)values(%s,%s,%s)"
            mycursor.execute(command,(user_id,username,action))
            mydb.commit()
        except:
            messagebox.showerror("Failed","Couldn't to log action")

    def redirect_to_home(self,username, role):
        # Destroy current window and create Home instance
        self.destroy()
        from homepage import Home
        home_page = Home(username=username,role=role) 
        home_page.mainloop()
    
    
    def redirect_to_Adminhome(self,username, role):
        # Destroy current window and create Home instance
        self.destroy()
        from AdminHomepage import AdminHome
        home_page = AdminHome(username=username, role=role) 
        home_page.mainloop()
    
    
    def redirect_to_EditProfile(self, username, role, stored_pass_hash, salt):
        # Destroy current window and create Home instance
        self.destroy()
        from EditNewProfile import NewProfile
        edit_page = NewProfile(username=username, role=role, stored_pass_hash=stored_pass_hash, salt=salt) 
        edit_page.mainloop()

    def go_to_signup(self): ## Function to transition to the sign-up page
        self.destroy()
        from signup import Signup
        signup = Signup()
        signup.mainloop()   
            

if __name__ == "__main__":
    app = Login()
    app.mainloop()
