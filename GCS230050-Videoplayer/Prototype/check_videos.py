import tkinter as tk
import tkinter.scrolledtext as tkst

import video_library as lib # load the video database from video_library.py
import font_manager as fonts # font_manager is the place where you control the fonts of whole application

def set_text(text_area , content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0 , content)

class CheckVideos():
    def __init__(self , window):
        window.geometry("750x350") # create a 750 x 350 window
        window.title("Check Video") # The title of the window is "Check Video"  

        # create a list video button and then show it on the window
        list_video_btn = tk.Button(window , text = "List All Videos" , command= self.list_videos_clicked)
        list_video_btn.grid(row = 0 , column = 0 , padx = 10 , pady = 10 )

        # create a label, the label show the content "Enter video Number" this is show the place user enter the video number
        enter_video_label = tk.Label(window , text = "Enter Video Number");
        enter_video_label.grid(row = 0 , column = 1 , padx = 10 , pady = 10)
        # create a entry, which called input_txt the user enter the text which is the video number
        self.input_txt = tk.Entry(window , width = 3)
        self.input_txt.grid(row = 0 , column = 2  , padx = 10 , pady = 10)
        # create a check videos button if the user click this button, it will call the attribute name check_videos_clicked
        check_videos_btn = tk.Button(window , text = "Check video" , command = self.check_videos_clicked)
        check_videos_btn.grid(row = 0 , column = 3 , padx = 10 , pady = 10)
        # the scrolledtext area where the application show the list of video 
        self.list_videos = tkst.ScrolledText(window , width = 48  , height = 12 , wrap = "none")
        self.list_videos.grid(row = 1 , column = 0 , columnspan = 3, sticky= "W" , padx = 10 , pady = 10)

        # this text area show the details of the movie
        self.video_txt = tk.Text(window , width = 24 , height = 4 , wrap = "none")
        self.video_txt.grid(row = 1 , column = 3 , sticky = "NW" , padx = 10 , pady = 10)

        # this show the status of the user whenever user interact with the application
        self.status_label = tk.Label(window , text = "" , font = ("Helvetical" , 10) )
        self.status_label.grid(row = 2 , column = 0 , columnspan= 4 , sticky= "SW" , padx = 10  , pady = 10)
        
        self.list_videos_clicked


    def list_videos_clicked(self):
        # the function will get all the video name from the library and then show it on the scrolled text area
        video_list = lib.list_all()
        set_text(self.list_videos , video_list)     
        self.status_label.configure(text = "List Videos button clicked")
    def is_number(self, key):
        try:
            int(key)
            return True
        except ValueError:
            return False
    
    def check_videos_clicked(self):
        # the function will get the id number from input_txt entry and then search the key and show it on the video_details text area
        key = self.input_txt.get()
        if not self.is_number(key):
            self.status_label.configure(text = "Please enter a number")
            return
        key = int(key)
        name= lib.get_name(key)
        if(name is not None):
            director = lib.get_director(key)    
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}"
            set_text(self.video_txt, video_details)
        else:
            set_text(self.video_txt, f"Video {key} not found")
        self.status_label.configure(text = "Check Videos button clicked")


if(__name__ == "__main__"):
    window = tk.Tk()
    fonts.configure()
    CheckVideos(window)
    window.mainloop()