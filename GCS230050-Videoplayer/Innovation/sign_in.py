import tkinter as tk
import csv
from tkinter import font
from video_player import VideoPlayer
from account_detail import db
import ttkbootstrap as ttkbs
import font_manager as font
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class Application(ttkbs.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("550x400")
        self.title("Authentication")
        self.account = {}

        # Load account data
        self.load_account_data()

        self.username = ""  # username
        self.password = ""  # password

        self.init_login_frame()
        self.init_signup_frame()

        self.show_login_frame()

    def load_account_data(self):
        try:
            with open("account.csv", "r", newline="") as csv_file:
                c = csv.reader(csv_file)
                for row in c:
                    if row[0] is not None:
                        self.account[row[0]] = row[1]
        except FileNotFoundError:
            pass  # Handle case where file does not exist

    def init_login_frame(self):
        self.login_frame = ttkbs.Frame(self)
        
        # Title
        title_lbl = ttkbs.Label(self.login_frame , bootstyle = "Active" , text="Welcome back!", font=("Timesnewroman", 16, "bold"))
        title_lbl.pack(side="top", pady=20)

        form_frame = ttkbs.Frame(self.login_frame)
        form_frame.pack(pady=10)

        # Username
        enter_user_name_lbl = ttkbs.Label(form_frame, text="Enter User Name: ", compound="center")
        enter_user_name_lbl.grid(row=0, column=0, padx=5, pady=10, sticky="e")

        self.username_txt = ttkbs.Entry(form_frame, width=30)
        self.username_txt.grid(row=0, column=1, padx=5, pady=10)

        # Password
        enter_password_lbl = ttkbs.Label(form_frame, text="Enter Password: ", compound="center")
        enter_password_lbl.grid(row=1, column=0, padx=5, pady=10, sticky="e")

        self.password_txt = ttkbs.Entry(form_frame, show="*", width=30)
        self.password_txt.grid(row=1, column=1, padx=5, pady=10)

        # Sign in button
        sign_in_button = ttkbs.Button(self.login_frame, bootstyle = "danger" ,text="Sign in", command=self.sign_in_clicked, style="success.TButton")
        sign_in_button.pack(side="top", padx=5, pady=10)

        self.login_status_lbl = ttkbs.Label(self.login_frame, text="", font=("Helvetica", 10))
        self.login_status_lbl.pack(side="top", padx=5, pady=10)

        # Sign up button
        sign_up_button = ttkbs.Button(self.login_frame, text="Sign Up here",bootstyle = "danger", command=self.show_signup_frame, style="link.TButton")
        sign_up_button.pack(side="top", padx=5, pady=10)

    def init_signup_frame(self):
        self.signup_frame = ttkbs.Frame(self)

        # Title
        title_lbl = ttkbs.Label(self.signup_frame, text="Sign Up", font=("Helvetica", 16, "bold"))
        title_lbl.pack(side="top", pady=20)

        form_frame = ttkbs.Frame(self.signup_frame)
        form_frame.pack(pady=10)

        # Username
        enter_user_name_lbl = ttkbs.Label(form_frame, text="Enter User Name: ", compound="center")
        enter_user_name_lbl.grid(row=0, column=0, padx=5, pady=10, sticky="e")

        self.signup_username_txt = ttkbs.Entry(form_frame, width=30)
        self.signup_username_txt.grid(row=0, column=1, padx=5, pady=10)

        # Password
        enter_password_lbl = ttkbs.Label(form_frame, text="Enter Password: ", compound="center")
        enter_password_lbl.grid(row=1, column=0, padx=5, pady=10, sticky="e")

        self.signup_password_txt = ttkbs.Entry(form_frame, show="*", width=30)
        self.signup_password_txt.grid(row=1, column=1, padx=5, pady=10)

        # Confirm password
        enter_password_confirm_lbl = ttkbs.Label(form_frame, text="Confirm Password: ", compound="center")
        enter_password_confirm_lbl.grid(row=2, column=0, padx=5, pady=10, sticky="e")

        self.signup_password_confirm_txt = ttkbs.Entry(form_frame, show="*", width=30)
        self.signup_password_confirm_txt.grid(row=2, column=1, padx=5, pady=10)

        # Sign up button
        sign_up_button = ttkbs.Button(self.signup_frame, text="Sign Up", command=self.sign_up_clicked, style="success.TButton")
        sign_up_button.pack(side="top", padx=5, pady=10)

        self.signup_status_lbl = ttkbs.Label(self.signup_frame, text="", font=("Helvetica", 10))
        self.signup_status_lbl.pack(side="top", padx=5, pady=10)

        # Back to login button
        back_to_login_button = ttkbs.Button(self.signup_frame, text="Back to Login", command=self.show_login_frame, style="link.TButton")
        back_to_login_button.pack(side="top", padx=5, pady=10)

    def clear_all(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_frame(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack()

    def show_signup_frame(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack()
    def sign_in_clicked(self):
        self.reset_signup()
        self.username = self.username_txt.get()
        self.password = self.password_txt.get()

        if not self.username and not self.password:
            self.login_status_lbl.configure(text="Username and password cannot be empty!")
            return
        if not self.username:
            self.login_status_lbl.configure(text="Username cannot be empty!")
            return
        if not self.password:
            self.login_status_lbl.configure(text="Password cannot be empty!")
            return
        if self.username in self.account:
            if self.account[self.username] == self.password:
                db.user_name = self.username
                db.first_time = False
                db.load_data()
                self.clear_all()
                VideoPlayer(self)
                # self.destroy()
                # self.withdraw()
                # return
            else:
                self.login_status_lbl.configure(text="Incorrect password!")
                self.password_txt.delete(0, tk.END)
                return
        else:
            self.login_status_lbl.configure(text="Username not found!")

    def sign_up_clicked(self):
        self.reset_login()
        username = self.signup_username_txt.get()
        password = self.signup_password_txt.get()
        password_confirm = self.signup_password_confirm_txt.get()
        
        if not username and not password and not password_confirm:
            self.signup_status_lbl.configure(text="Username and password cannot be empty!")
            return
        if not password and not password_confirm:
            self.signup_status_lbl.configure(text="Password and password confirmation cannot be empty!")
            return
        if not username:
            self.signup_status_lbl.configure(text="Username cannot be empty!")
            return
        if not password:
            self.signup_status_lbl.configure(text="Password cannot be empty!")
            return
        if not password_confirm:
            self.signup_status_lbl.configure(text="Password confirmation cannot be empty!")
            return
        if username in self.account:
            self.signup_status_lbl.configure(text="Username already exists!")

            return
        if password == password_confirm:
            self.account[username] = password
            with open("account.csv", "w", newline="") as csv_file:
                c = csv.writer(csv_file)
                for key, value in self.account.items():
                    c.writerow([key, value])
            db.user_name = username
            db.first_time = True
            db.load_data()
            db.save_data()
            self.signup_status_lbl.configure(text="Account created successfully. Please log in.")
            self.show_login_frame()
        else:
            self.signup_status_lbl.configure(text="Passwords do not match!")
            self.signup_password_txt.delete(0, tk.END)
            self.signup_password_confirm_txt.delete(0, tk.END)

    def reset_login(self):
        self.username_txt.delete(0, tk.END)
        self.password_txt.delete(0, tk.END)
        self.login_status_lbl.configure(text="")

    def reset_signup(self):
        self.signup_username_txt.delete(0, tk.END)
        self.signup_password_txt.delete(0, tk.END)
        self.signup_password_confirm_txt.delete(0, tk.END)
        self.signup_status_lbl.configure(text="")

if __name__ == "__main__":
    theme = "cyborg"
    window = Application(themename=theme)
    window.mainloop()
