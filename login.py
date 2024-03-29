import customtkinter as ct
import tkinter as ttk
from tkinter import messagebox
import PIL 
from PIL import ImageTk, Image
import mysql.connector as msql
import bcrypt
from Crypto.Util.number import long_to_bytes

username=''
ct.set_appearance_mode("dark")  
ct.set_default_color_theme("green")

img = PIL.Image.open("./Assets_Cat/loginAdoption.jpg") # change to match repo of image



class Login(ct.CTk):
    def __init__(self):
        super().__init__()
        global username
        self.title("Login")
        self.geometry("1280x1100")

        ### Load the background image
        self.background_image_original = Image.open("./Assets_Cat/loginAdoption.jpg")

        ### Create a PhotoImage object from the original background image
        self.background_image = ImageTk.PhotoImage(self.background_image_original)

        ### Create a copy of the background image for resizing
        self.background_image_copy = self.background_image_original.copy()
        
        ### Create and configure the background label
        self.background_label = ct.CTkLabel(master=self, image=self.background_image)
        self.background_label.pack(fill="both", expand=True)
        self.background_label.bind('<Configure>', self._resize_image)
        




        
        self.frame1 = ct.CTkFrame(self, height=500, width=400)
        self.frame1.pack(pady=5)


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

        # Label for forget password
        self.forget_password_label = ct.CTkLabel(self, text="Forget password?", font=('Century Gothic', 12))
        self.forget_password_label.place(x=250, y=180)
        
        self.button1 = ct.CTkButton(self.frame1, text="login", command=self.login_check, image=ct.CTkImage(dark_image=img, light_image=img))
        self.button1.pack(pady=40, padx=120)
            
    # Function to resize the background image (cat image)
    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the background image copy
        resized_image = self.background_image_copy.resize((new_width, new_height))

        # Convert the resized image to PhotoImage format
        resized_photo_image = ImageTk.PhotoImage(resized_image)

        # Configure the background label to display the resized image
        self.background_label.configure(image=resized_photo_image)


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
                                user='root',# change username to match your database user
                                password='Bella*8234', # change pass
                                database='new_schema')# change database to match your database name
                mycursor=mydb.cursor()
                #messagebox.showerror("","Connected to database")
                command = "use new_schema"
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