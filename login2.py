import tkinter
from tkinter import messagebox
import customtkinter
from PIL import ImageTk, Image
import mysql.connector as msql



class LoginApp:
    def __init__(self):
        self.app = customtkinter.CTk()  # Creating custom tkinter window
        self.app.geometry("600x440")
        self.app.title('Login')

        self.imagee = Image.open("cat.png")

        self.img1 = ImageTk.PhotoImage(self.imagee)
        self.img_copy=Image.open("cat.png").copy()
        
        self.l1 = customtkinter.CTkLabel(master=self.app, image=self.img1)
        self.l1.pack(fill="both", expand=True)
        self.l1.bind('<Configure>', self._resize_image)
        # Creating custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.l2 = customtkinter.CTkLabel(master=self.frame, text="Log into your Account", font=('Century Gothic', 20))
        self.l2.place(x=50, y=45)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.entry1.place(x=50, y=110)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*")
        self.entry2.place(x=50, y=165)

        self.l3 = customtkinter.CTkLabel(master=self.frame, text="Forget password?", font=('Century Gothic', 12))
        self.l3.place(x=155, y=195)

        # Create custom button
        self.button1 = customtkinter.CTkButton(master=self.frame, width=220, text="Login", command=self.button_function, corner_radius=6)
        self.button1.place(x=50, y=240)

        self.img2 = customtkinter.CTkImage(Image.open("cat.png").resize((5, 5), Image.ADAPTIVE))
        self.img3 = customtkinter.CTkImage(Image.open("cat.png").resize((5, 5), Image.ADAPTIVE))
        self.button2 = customtkinter.CTkButton(master=self.frame, image=self.img2, text="Google", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
        self.button2.place(x=50, y=290)

        self.button3 = customtkinter.CTkButton(master=self.frame, image=self.img3, text="Facebook", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
        self.button3.place(x=170, y=290)

        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()

        self.label2 = customtkinter.CTkLabel(master=self.frame, text="", font=('Century Gothic', 12))
        self.label2.place(x=50, y=320)
        self.app.mainloop()

    def button_function(self):
        username = self.entry1.get()
        password = self.entry2.get()
       ## salt = bcrypt.gensalt()
      ##  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
       ## print(salt," //// ", hashed_password)
        if not (username) or not (password):
            self.label2.configure(text="please enter username and password")
            messagebox.showerror("Error", "Type Username and Password")
        else:
            try:
                # database credentials and information ... i named it new_schema .. you can name it whatever you want
                mydb = msql.connect(host="localhost",
                                    user='root',  # change username to match your database user
                                    password='Bella*8234',  # change pass
                                database='new_schema')  # change database to match your database name
                mycursor = mydb.cursor()
                # messagebox.showerror("","Connected to database")
                command = "use new_schema"
                mycursor.execute(command)
                # we will execute a command to get username and password from table (login) ... you can call the table whatever you want too
                command = "select * from login where username=%s and password=%s"  # change table name to match your target table name
                mycursor.execute(command, (username, password))  # first and second %s will be replaced with username and password passed into mycursor.execute()

                # fetches and returns a single query with the username and password we passed .... or returns None if not found
                myresult = mycursor.fetchone()
                if myresult is not None:
                    ##messagebox.showerror("Success", "Login Successful")
                    self.label2.configure(text="Login Successful")
                    self.app.destroy()            # destroy current window and creating new one 
                    w = customtkinter.CTk()  
                    w.geometry("1280x720")
                    w.title('Welcome')
                    l1=customtkinter.CTkLabel(master=w, text="welcome "+username ,font=('Century Gothic',60))
                    l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
                    w.mainloop()
                else:
                    messagebox.showerror("Failed", "Login Failed")
                    self.label2.configure(text="Login Failed")
            except:
                messagebox.showerror("Failed", "Couldn't connect to database")

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.imagee = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.imagee)
        self.l1.configure(image = self.background_image)



app = LoginApp()
app.mainloop()