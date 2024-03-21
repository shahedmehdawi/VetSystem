import tkinter
from tkinter import messagebox
import customtkinter as ct
from PIL import ImageTk, Image
import mysql.connector as msql
import bcrypt
from bcrypt import hashpw
from bcrypt import*


class LoginApp(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x440")
        self.title('Login')

        ### Load the background image
        self.background_image_original = Image.open("./Desktop/tkinter/cat.png")

        ### Create a PhotoImage object from the original background image
        self.background_image = ImageTk.PhotoImage(self.background_image_original)

        ### Create a copy of the background image for resizing
        self.background_image_copy = self.background_image_original.copy()
        
        ### Create and configure the background label
        self.background_label = ct.CTkLabel(master=self, image=self.background_image)
        self.background_label.pack(fill="both", expand=True)
        self.background_label.bind('<Configure>', self._resize_image)
        
        # Creating custom frame
        self.login_frame = ct.CTkFrame(master=self.background_label, width=320, height=360, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Label for login title
        self.login_title_label = ct.CTkLabel(master=self.login_frame, text="Log into your Account", font=('Century Gothic', 20))
        self.login_title_label.place(x=50, y=45)

        # Entry widget for username
        self.username_entry = ct.CTkEntry(master=self.login_frame, width=220, placeholder_text='Username')
        self.username_entry.place(x=50, y=110)

        # Entry widget for password
        self.password_entry = ct.CTkEntry(master=self.login_frame, width=220, placeholder_text='Password', show="*")
        self.password_entry.place(x=50, y=165)

        # Label for forget password
        self.forget_password_label = ct.CTkLabel(master=self.login_frame, text="Forget password?", font=('Century Gothic', 12))
        self.forget_password_label.place(x=155, y=195)

        # Button for login
        self.login_button = ct.CTkButton(master=self.login_frame, width=220, text="Login", command=self.button_function, corner_radius=6)
        self.login_button.place(x=50, y=240)

        # Custom buttons for Google and Facebook
        self.google_image = ct.CTkImage(Image.open("./Desktop/tkinter/cat.png").resize((5, 5), Image.ADAPTIVE))
        self.facebook_image = ct.CTkImage(Image.open("./Desktop/tkinter/cat.png").resize((5, 5), Image.ADAPTIVE))
        self.google_button = ct.CTkButton(master=self.login_frame, image=self.google_image, text="Google", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
        self.google_button.place(x=50, y=290)

        self.facebook_button = ct.CTkButton(master=self.login_frame, image=self.facebook_image, text="Facebook", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
        self.facebook_button.place(x=170, y=290)

        # Variables for username and password
        self.username_var = tkinter.StringVar()
        self.password_var = tkinter.StringVar()

        # Label for error message
        self.error_label = ct.CTkLabel(master=self.login_frame, text="", font=('Century Gothic', 12))
        self.error_label.place(x=50, y=320)
        self.mainloop()  
    
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


    def button_function(self):
        username = self.entry1.get()
        password = self.entry2.get()

        if not (username) or not (password):
            self.label2.configure(text="Please enter username and password")
            messagebox.showerror("Error", "Type Username and Password")
        else:
            try:
                # Connect to the database
                mydb = msql.connect(host="localhost",
                                    user='root',
                                    password='Bella*8234',
                                    database='new_schema')
                mycursor = mydb.cursor()

                # Query to fetch salt and hashed password from the database based on the provided username
                command = "SELECT password, salt FROM login2 WHERE username = %s"
                mycursor.execute(command, (username,))
                row = mycursor.fetchone()

                if row is not None:
                    hashed_password_fromDB= row[0]
                    salt_fromDB= row[1]

                    # Hash the input password using the retrieved salt
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt_fromDB)

                    # Check if the hashed password matches the hashed password from the database
                    if bcrypt.checkpw(hashed_password, hashed_password_fromDB):
                        self.label2.configure(text="Login Successful")
                        self.app.destroy()
                        new_window = ct.CTk()  ## creating new window after destroying the previous one
                        new_window.geometry("1280x720")
                        new_window.title('Welcome')
                        label1=ct.CTkLabel(master=new_window, text="welcome "+username ,font=('Century Gothic',60))
                        label1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
                        new_window.mainloop()

                    else:
                        messagebox.showerror("Failed", "Login Failed")
                        self.label2.configure(text="Login Failed")
                else:
                    messagebox.showerror("Failed", "User not found")
                    self.label2.configure(text="User not found")
            except:
                messagebox.showerror("Failed", "Couldn't connect to database")





app = LoginApp()
app.mainloop()