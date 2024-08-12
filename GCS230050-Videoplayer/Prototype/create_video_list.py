import tkinter as tk
import tkinter.scrolledtext as tkst

import video_library as lib  # load the video database from video_library.py
import font_manager as fonts  # font_manager is the place where you control the fonts of whole application
from account_detail import db

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class Create_play_list():
    def __init__(self, window):
        self.video_play_lists = []
        self.text_for_show = ""

        window.geometry("1150x550")  # create a 1050 x 550 window
        window.title("Create Video List")  # The title of the window is "Check Video"
        for i in range(0 , len(db.playlist)):
            if(db.playlist[i] == 1):
                self.text_for_show = self.text_for_show + f"{i} {lib.get_name(i)}-{lib.get_director(i)}\n"
                self.video_play_lists.append(i)
       # FRAME

        # Top tool bar frame
        toolbar = tk.Frame(window)
        toolbar.pack(side="top", padx=5, pady=10)

        # Display area setting frame
        display = tk.Frame(window)
        display.pack(side="top", padx=5, pady=5)

        # Play area frame
        playarea = tk.Frame(window)
        playarea.pack(side="top", padx=10, pady=5)

        # TOOL BAR
        # List video button
        list_video_btn = tk.Button(toolbar, text="List All Videos", compound="center", padx=0, pady=0, command=self.list_videos_clicked)
        list_video_btn.pack(side="left", padx=60)

        enter_video_lbl = tk.Label(toolbar, text="    Video Number ", compound="center", padx=0, pady=0)
        enter_video_lbl.pack(side="left")

        self.input_txt = tk.Entry(toolbar, width=3)  # Entry for the video number
        self.input_txt.pack(side="left")

        # Add video to the playlist button
        add_to_list_btn = tk.Button(toolbar, text="Add", compound="center", padx=10, pady=0, command=self.add_videos_clicked)
        add_to_list_btn.pack(side="left", padx=25)
        # Play video from the playlist button
        play_playlist_btn = tk.Button(toolbar, text="Play", compound="center", padx=20, pady=0, command=self.play_video)
        play_playlist_btn.pack(side="left", padx=50)
        # create a clear button to clear all the video in the playlist
        reset_button = tk.Button(toolbar, text="Reset Playlist", command=self.clear_play_list)
        reset_button.pack(side="right")



        # DISPLAY AREA
        # Display video list area
        self.list_videos = tkst.ScrolledText(display, wrap="none")
        self.list_videos.pack(side="left", padx=5, pady=2)
        # Playlist area to display videos
        self.video_txt = tkst.ScrolledText(display, wrap="none")
        self.video_txt.pack(side="left", padx=5, pady=2)
        set_text(self.video_txt , self.text_for_show)
        self.status_label = tk.Label(window, text="", font=("Helvetica", 10))  # Label to display status information
        self.status_label.pack(side="bottom", padx=10, pady=1)


    def list_videos_clicked(self):
        # the function will get all the video name from the library and then show it on the scrolled text area
        video_list = lib.list_all()
        set_text(self.list_videos, video_list)
        self.status_label.configure(text="List Videos button was clicked!")
    def check_digit(self, key):
        try:
            key = int(key)
            return True
        except:
            return False
    def add_videos_clicked(self):
        # the function will get the video number
        key = self.input_txt.get()
        if not self.check_digit(key):
            self.status_label.configure(text = "Please enter a valid number!")
            return
        key = int(key)
        ok = False
        name = lib.get_name(key)
        if key not in self.video_play_lists:
            if name is not None:
                self.video_play_lists.append(key)
                ok = True
            else:
                self.status_label.configure(text="Cannot find the video!")
        else:
            self.status_label.configure(text="Video already in play list!")
        if ok:
            self.text_for_show = self.text_for_show + f"{key} {name}-{lib.get_director(key)}\n"
            set_text(self.video_txt, self.text_for_show)
            db.playlist[key] = 1
            self.status_label.configure(text="Video was added to play list!")
            db.save_data()

    def clear_play_list(self):
        if(not len(self.video_play_lists)):
            return
        self.text_for_show = ""
        self.video_play_lists = []
        for i in range(0 , len(db.playlist)):
            if(db.playlist[i] == 1):
                db.playlist[i] = 0
        db.save_data()
        set_text(self.video_txt , self.text_for_show)
        self.status_label.configure(text="Play list was cleared!")
    
    def play_video(self):
        if(not len(self.video_play_lists)):
            return    
        for x in self.video_play_lists:
            lib.increment_play_count(x)
        lib.save_data()
        self.status_label.configure(text="Playing videos! Play button was clicked!")
if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    Create_play_list(window)
    window.mainloop()
