import tkinter as tk


import font_manager as fonts
from check_videos import CheckVideos
from create_video_list import Create_play_list
from update_videos import update_videos
from account_detail import db

class Video_player():  
    def __init__(self , window):
        window.geometry("520x150")
        window.title("Video Player")
        fonts.configure()
        self.header_lbl = tk.Label(window, text="Select an option by clicking one of the buttons below")
        self.header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        check_videos_btn = tk.Button(window, text="Check Videos", command=self.check_videos_clicked)
        check_videos_btn.grid(row=1, column=0, padx=10, pady=10)

        create_video_list_btn = tk.Button(window, text="Create Video List", command =self.create_play_lists_clicked)
        create_video_list_btn.grid(row=1, column=1, padx=10, pady=10)

        update_videos_btn = tk.Button(window, text="Update Videos" , command = self.update_videos_clicked)
        update_videos_btn.grid(row=1, column=2, padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.status_lbl.configure(text = f"Welcome {db.user_name}!")
    def check_videos_clicked(self):
        self.status_lbl.configure(text="Check Videos button was clicked!")
        CheckVideos(tk.Toplevel())
    def create_play_lists_clicked(self):
        self.status_lbl.configure(text = "Create Video List clicked!")
        Create_play_list(tk.Toplevel())

    def update_videos_clicked(self):
        self.status_lbl.configure(text ="Update Videos button was clicked!")
        update_videos(tk.Toplevel())
