import tkinter as tk
import csv
from tkinter import font
import tkinter.scrolledtext as tkst
import font_manager as fonts
from video_player import Video_player
from sign_up import Sign_up
from account_detail import db
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class login():
    def __init__(self , window):
        fonts.configure()
        self.window = window
        self.window.geometry("550x400")  # create a 1050 x 550 window
        self.window.title("Sign In")
        self.account = {}
        csv_file = open("account.csv" , "r" , newline = "")
        c = csv.reader(csv_file)
        for row in c:
            if(row[0] is not None):
                self.account[row[0]] = row[1]
        csv_file.close()
        self.username = "" # username
        self.password = "" # password
        enter_user_name_lbl = tk.Label(self.window, text="Enter User Name: ", compound="center", padx=0, pady=0)
        enter_user_name_lbl.pack(side="top", padx=5, pady=10)
        self.username_txt = tk.Entry(self.window, width=30)
        self.username_txt.pack(side="top", padx=5, pady=10)
        enter_password_lbl = tk.Label(self.window, text="Enter Password: ", compound="center", padx=0, pady=0)
        enter_password_lbl.pack(side="top", padx=5, pady=10)
        self.password_txt = tk.Entry(self.window, show="*", width=30)
        self.password_txt.pack(side="top", padx=5, pady=10)
        # Sign up button
        sign_in_button = tk.Button(self.window, text="Sign in", command=self.sign_in_clicked)
        sign_in_button.pack(side="top", padx=5, pady=10)
        self.status_lbl = tk.Label(self.window, text="", font=("Helvetica", 10))
        self.status_lbl.pack(side="top", padx=5, pady=10)
        # don't have an account sign up button
        sign_up_button = tk.Button(self.window, text="Sign Up here", command=self.sign_up_clicked)
        sign_up_button.pack(side="top", padx=5, pady=10)

    def sign_up_clicked(self):
        self.window.destroy()
        Sign_up(tk.Tk())
        return
    def sign_in_clicked(self):
        self.username = self.username_txt.get()
        self.password = self.password_txt.get()
        if(self.username == "" and self.password == ""):
            self.status_lbl.configure(text = "Username and password cannot be empty!")
            return
        if(self.username == ""):
            self.status_lbl.configure(text = "Username cannot be empty!")
            return
        if(self.password == ""):
            self.status_lbl.configure(text = "Password cannot be empty!")
            return
        if(self.username in self.account):
            if(self.account[self.username] == self.password):
                db.user_name = self.username   
                db.first_time = False 
                db.load_data()
                self.window.destroy()
                Video_player(tk.Tk())
                return
            else:
                self.status_lbl.configure(text = "Incorrect password!")
                self.password_txt.delete(0, tk.END)
                return
        else:
            self.status_lbl.configure(text = "Username not found!")
            self.reset_clicked()
    def reset_clicked(self):
        self.username_txt.delete(0, tk.END)
        self.password_txt.delete(0, tk.END)
if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    login(window)
    window.mainloop()