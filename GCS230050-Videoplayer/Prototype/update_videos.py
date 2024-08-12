import tkinter as tk
import tkinter.scrolledtext as tkst

import video_library as lib  # load the video database from video_library.py
import font_manager as fonts  # font_manager is the place where you control the fonts of whole application
from account_detail import db

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class update_videos():
    def __init__(self, window):
        self.video_play_lists = []
        self.text_for_show = ""

        window.geometry("1050x550")  # create a 1050 x 550 window
        window.title("Update Videos")  # The title of the window is "Check Video"


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
        list_video_btn.pack(side="left", padx=30)

        enter_video_lbl = tk.Label(toolbar, text="Video Number ", compound="center", padx=0, pady=0)
        enter_video_lbl.pack(side="left")

        self.input_txt = tk.Entry(toolbar, width=3)  # Entry for the video number
        self.input_txt.pack(side="left" , padx = 10)

        # Rating inputs
        new_rating_lbl = tk.Label(toolbar , text = "New rating:" , compound= "center", padx = 0 , pady = 0)
        new_rating_lbl.pack(side = "left")
        # rating text
        self.new_rating_txt = tk.Entry(toolbar , width = 3)
        self.new_rating_txt.pack(side = "left" , padx = 55)

        # create a clear button to clear all the video in the playlist
        update_button = tk.Button(toolbar, text="Update Video", padx = 10 , pady = 0 , command=self.update_videos_rating)
        update_button.pack(side="right")



        # DISPLAY AREA
        # Display video list area
        self.list_videos = tkst.ScrolledText(display, wrap="none")
        self.list_videos.pack(side="left", padx=5, pady=2)
        # Playlist area to display videos
        self.video_txt = tkst.ScrolledText(display, wrap="none")
        self.video_txt.pack(side="left", padx=5, pady=2)

        self.status_label = tk.Label(window, text="", font=("Helvetica", 10))  # Label to display status information
        self.status_label.pack(side="bottom", padx=10, pady= 0)

    def check_integer(self, st): # check the string is integer or not
        for i in range(0 , len(st)):
            if(st[i] < '0' or st[i] > '9'):
                return False
        return True
    
    def list_videos_clicked(self):
        # the function will get all the video name from the library and then show it on the scrolled text area
        video_list = lib.list_all()
        set_text(self.list_videos, video_list)
        self.status_label.configure(text="List Videos button was clicked!")

    def update_videos_rating(self):
        key = self.input_txt.get()
        if not self.check_integer(key):
            self.status_label.configure(text = "Please enter a number for video id!")
            return
        key = int(key)
        name = lib.get_name(key)
        if(name is not None): # check if the id is valid
            new_rating = self.new_rating_txt.get()
            if(self.check_integer(new_rating)): # check if the input rating is valid
                new_rating = int(new_rating)
                # check the rating is >= 1 and <= 5
                if(1 <= new_rating and new_rating <= 5):
                    # update the new_rating
                    if(db.user_rate[key] != 0):
                        lib.new_rating_update(key , new_rating)
                        db.user_rate[key] = new_rating

                    else:
                        lib.library[key].total_of_rating -= db.user_rate[key]
                        lib.library[key].total_of_rating += new_rating
                        db.user_rate[key] = new_rating            
                        lib.library[key].rating = lib.library[key].total_of_rating / lib.library[key].number_of_rate_time
                    db.save_data()
                    self.status_label.configure(text = "Rating updated!")
                    # show the name , rating and number of play count
                    set_text(self.video_txt, f"{name}\nRating: {lib.get_rating(key)}\nPlay count: {lib.get_play_count(key)}")
                    # update the video_list
                    video_list = lib.list_all()
                    set_text(self.list_videos , video_list)
                    lib.save_data()
                else:
                    self.status_label.configure(text = "Rating must be an integer, greater than 0 and less than 6!")
            else:
                self.status_label.configure(text = "Rating must be an integer, greater than 0 and less than 6!")
                
        else:
            self.status_label.configure(text = "Can not find video!")


if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    update_videos(window)
    window.mainloop()
