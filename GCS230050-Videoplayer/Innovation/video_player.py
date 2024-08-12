from tkinter import *  # Import all from tkinter
import tkinter as tk
import csv
from account_detail import db
import ttkbootstrap as tb
import math
from ttkbootstrap.scrolled import ScrolledFrame
import video_library as lib  # load the video database from video_library.py
import font_manager as fonts  # font_manager is the place where you control the fonts of whole application
from PIL import Image, ImageTk
from add_to_playlist import AddToPlaylist

class VideoPlayer():
    def __init__(self, window):
        self.window = window
        self.rate_tab = None # Initialize rate tab attribute
        fonts.configure()
        # Window settings
        self.window.title("Video Player")
        self.window.geometry("1760x990")
        self.which_tab = 0  # tab 0 for video list, tab 1 is the playlist, tab 2 is the search tab, tab 3 for rate
        self.playlist_tab = None  # Initialize playlist_tab attribute

        # Frame setup
        # Top Frame
        self.topFrame = tb.Frame(self.window, bootstyle="Active")  # Create a frame with Active bootstyle
        self.topFrame.pack(side="top", fill="x")

        # Top Left Frame
        self.leftTopFrame = tb.Frame(self.topFrame, bootstyle="Active")  # Create a frame with Active bootstyle")
        self.leftTopFrame.pack(side="left", padx=10)

        # App Icon
        appIcon = tb.Label(self.leftTopFrame, text="NETFLIX", bootstyle="danger", compound="left", font=("Helvetica", 24, "bold"))
        appIcon.pack(side="left", pady=10)

        # Top Middle Frame
        self.middleTopFrame = tb.Frame(self.topFrame, bootstyle="Active")  # Create a frame with Active bootstyle")
        self.middleTopFrame.pack(side="left", padx=40, expand=True)

        # Top Right Frame
        rightTopFrame = tb.Frame(self.topFrame, bootstyle="Active")  # Create a frame with Active bootstyle")
        rightTopFrame.pack(side="right", padx=55)

        # Display Frame
        self.displayFrame = ScrolledFrame(self.window, bootstyle="Active")  # Create a frame with Active bootstyle)
        self.displayFrame.pack(side="left", padx=150, pady=0, fill="both", expand=YES)

        # Video List
        self.videoList = tb.LabelFrame(self.displayFrame, text="Video List", bootstyle="danger")
        self.videoList.pack(side="bottom", padx=10, pady=0, fill="both")

        # When user presses enter, it will search the video
        self.window.bind('<Return>', lambda event: self.enterbutton_pressed())

        # Combobox for search type
        self.selectSearchType = tb.Combobox(self.middleTopFrame, textvariable="value", state="readonly", width=10, bootstyle="danger")
        self.selectSearchType["value"] = ("Video ID", "Title", "Director")
        self.selectSearchType.current(0)
        self.selectSearchType.pack(side="left", padx=5)

        # Search bar
        self.searchBar = tb.Entry(self.middleTopFrame, bootstyle="danger", width=30)
        self.searchBar.pack(side="left", pady=25, padx=5)

        # Set different styles for star buttons
        self.bootstyleNotChoose = "link" # Bootstyle link-default, for a star if not choosing it
        self.bootstyleChoose = "link-warning" # Bootstyle link-warning, a yellow star if clicked

        # Search button
        self.searchButton = tb.Button(self.middleTopFrame, text="🔎", bootstyle="danger", command=self.search_video_click)
        self.searchButton.pack(side="left", padx=5)

        # Playlist tab combobox
        self.playlist_tab = tb.Combobox(self.middleTopFrame, textvariable="value2", state="readonly", width=10, bootstyle="danger")
        self.playlist_tab["value"] = db.playlist_name
        self.playlist_tab.current(0)
        self.playlist_tab.pack(side="left")

        # Filter button with icon (Unicode character for filter icon)
        self.chooseplaylist = tb.Button(self.middleTopFrame, text="✔", bootstyle="danger", command=self.open_playlist)
        self.chooseplaylist.pack(side="left", padx=5)

        # Add new playlist button with icon (Unicode character for plus icon)
        self.addPlaylistButton = tb.Button(self.middleTopFrame, text="➕", bootstyle="danger", command=self.add_new_playlist)
        self.addPlaylistButton.pack(side="left")

        # Reset button
        resetButton = tb.Button(rightTopFrame, text="↻", bootstyle="danger", command=self.all_video_clicked)
        resetButton.pack(side="left", padx=0, pady=0)

        self.all_video_clicked()

    def check_integer(self, st): # check if the string is an integer
        if(len(st) == 0): 
            return False
        for i in range(0, len(st)):
            if(st[i] < '0' or st[i] > '9'):
                return False
        return True

    def clear_frame(self):
        # Reset the scrollable frame
        for widget in self.videoList.winfo_children():
            widget.destroy()

    def enterbutton_pressed(self):
        if(self.searchBar.get() != ""):
            self.search_video_click()

    def all_video_clicked(self):
        self.clear_frame()
        self.which_tab = 0
        self.addPlaylistButton.configure(bootstyle="danger")
        self.searchBar.delete(0, 'end')  # Clear the search bar
        self.selectSearchType.current(0)
        self.playlist_tab.configure(bootstyle="danger")
        self.which_tab = 0
        self.chooseplaylist.configure(text="✔")
        self.playlist_tab["value"] = db.playlist_name
        self.playlist_tab.current(0)
        for object in lib.library:
            id = object
            videoname = lib.library[object].name
            rating = lib.library[object].rating
            tag = lib.library[object].tag
            length = lib.library[object].length
            year = lib.library[object].year
            director = lib.library[object].director
            # Create a frame for each video
            self.videoFrameTop = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
            self.videoFrameTop.pack(side="top", padx=10, pady=10, fill="x")  # Pack at the top with horizontal padding 10, vertical padding 10, filling horizontally
            videoIdInformation = f"     {id}.  "
            videoYearTimeInformation = f"     {year}  {math.floor(length/60)}h {length%60}m  {tag} \n     Director: {director}"
            videoRatingInformation = f"★{rating}"
            # Labels displaying video information
            tb.Label(self.videoFrameTop, text=videoIdInformation, bootstyle="default", justify="left").pack(side="left")  # Pack on the left with left justification
            tb.Label(self.videoFrameTop, text=videoname, bootstyle="default").pack(side="left", padx=0)  # Pack on the left with no horizontal padding
            self.videoFrameMiddle = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
            self.videoFrameMiddle.pack(side="top", padx=10, fill="x")  # Pack at the top with horizontal padding 10, filling horizontally
            tb.Label(self.videoFrameMiddle, text=videoYearTimeInformation, bootstyle="default").pack(side="left")  # Pack on the left
            self.videoFrameBottom = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
            self.videoFrameBottom.pack(side="top", padx=10, fill="x")  # Pack at the top with horizontal padding 10, filling horizontally
            tb.Label(self.videoFrameBottom, text=videoRatingInformation, bootstyle="default").pack(side="left", padx=60)  # Pack on the left with horizontal padding 60
            # Buttons and separators
            tb.Button(self.videoFrameMiddle, text="➕", bootstyle="link", command=lambda id=id: self.add_play_list(id)).pack(side="right", padx=40)  # Create a button with link bootstyle and a command callback, pack on the right with horizontal padding 40
            tb.Separator(self.videoFrameMiddle, bootstyle="Active")  # Create a frame with Active bootstyle", orient="vertical").pack(side="right", fill="y")  # Create a vertical separator with Active")  # Create a frame with Active bootstylebootstyle, pack on the right filling vertically
            self.infoButton = tb.Button(self.videoFrameMiddle, text="ℹ️", bootstyle="link", command=lambda id=id: self.video_info_and_rate_click(id, 0))  # Create a button with link bootstyle and a command callback
            self.infoButton.pack(side="right", padx=40)  # Pack on the right with horizontal padding 40
            self.rateStar = tb.Button(self.videoFrameBottom, text="☆ rate", bootstyle="link", command=lambda id=id: self.video_info_and_rate_click(id, 0))  # Create a button with link bootstyle and a command callback
            self.rateStar.pack(side="left", padx=10)  # Pack on the left with horizontal padding 10
            # Line separator
            self.lineFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
            self.lineFrame.pack(side="top", fill="x", pady=20)  # Pack at the top filling horizontally, with vertical padding 20
            tb.Separator(self.lineFrame, bootstyle="light", orient="horizontal").pack(side="bottom", fill="x", padx=20)  # Create a horizontal separator with light bootstyle, pack at the bottom filling horizontally, with horizontal padding 20

    # For playlist
    def open_playlist(self, each_video=0):
        self.clear_frame()
        ok = True
        self.chooseplaylist.configure(text="❌")
        playlist_name = self.playlist_tab.get()
        # Don't need which_tab variable
        self.addPlaylistButton.configure(bootstyle="danger")
        if each_video == 1:
            ok = False
        else:
            ok = self.which_tab == 1
        if not ok:
            self.playlist_tab.configure(bootstyle="danger")
            self.which_tab = 1
            if(playlist_name != "Playlist"):
                #delete playlist button
                delete_button =tb.Button(self.videoList, text="Delete play list❌", bootstyle="danger", command= lambda: self.delete_playlist_name(playlist_name))
                delete_button.pack(side="top", padx=10, pady=10)

            ok = False
            for object in lib.library:
                id = object
                if db.playlist[playlist_name][int(id)] == 1:
                    ok = True
                    videoname = lib.library[object].name
                    rating = lib.library[object].rating
                    tag = lib.library[object].tag
                    length = lib.library[object].length
                    year = lib.library[object].year
                    director = lib.library[object].director
                    # Create a frame for each video
                    self.videoFrameTop = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                    self.videoFrameTop.pack(side="top", padx=10, pady=10, fill="x")  # Pack at the top with horizontal padding 10, vertical padding 10, filling horizontally
                    videoIdInformation = f"     {id}.  "
                    videoYearTimeInformation = f"     {year}  {math.floor(length/60)}h {length%60}m  {tag} \n     Director: {director}"
                    videoRatingInformation = f"★{rating}"
                    # Labels displaying video information
                    tb.Label(self.videoFrameTop, text=videoIdInformation, bootstyle="default", justify="left").pack(side="left")  # Pack on the left with left justification
                    tb.Label(self.videoFrameTop, text=videoname, bootstyle="default").pack(side="left", padx=0)  # Pack on the left with no horizontal padding
                    self.videoFrameMiddle = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                    self.videoFrameMiddle.pack(side="top", padx=10, fill="x")  # Pack at the top with horizontal padding 10, filling horizontally
                    tb.Label(self.videoFrameMiddle, text=videoYearTimeInformation, bootstyle="default").pack(side="left")  # Pack on the left
                    self.videoFrameBottom = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                    self.videoFrameBottom.pack(side="top", padx=10, fill="x")  # Pack at the top with horizontal padding 10, filling horizontally
                    tb.Label(self.videoFrameBottom, text=videoRatingInformation, bootstyle="default").pack(side="left", padx=60)  # Pack on the left with horizontal padding 60

                    tb.Button(self.videoFrameMiddle, text="❌", bootstyle="link", command=lambda id=id: self.deletet_playlist(id, 1, playlist_name)).pack(side="right", padx=40)  # Create a button with link bootstyle and a command callback, pack on the right with horizontal padding 40
                    tb.Separator(self.videoFrameMiddle, bootstyle="Active")  # Create a frame with Active bootstyle", orient="vertical").pack(side="right", fill="y")  # Create a vertical separator with Active")  # Create a frame with Active bootstyle bootstyle, pack on the right filling vertically
                    self.infoButton = tb.Button(self.videoFrameMiddle, text="ℹ️", bootstyle="link", command=lambda id=id: self.video_info_and_rate_click(id, 1))  # Create a button with link bootstyle and a command callback
                    self.infoButton.pack(side="right", padx=40)  # Pack on the right with horizontal padding 40
                    self.rateStar = tb.Button(self.videoFrameBottom, text="☆ rate", bootstyle="link", command=lambda id=id: self.video_info_and_rate_click(id, 1))  # Create a button with link bootstyle and a command callback
                    self.rateStar.pack(side="left", padx=10)  # Pack on the left with horizontal padding 10
                    # Line separator
                    self.lineFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                    self.lineFrame.pack(side="top", fill="x", pady=20)  # Pack at the top filling horizontally, with vertical padding 20
                    tb.Separator(self.lineFrame, bootstyle="light", orient="horizontal").pack(side="bottom", fill="x", padx=20)  # Create a horizontal separator with light bootstyle, pack at the bottom filling horizontally, with horizontal padding 20
            if not ok:
                tb.Label(self.videoList, text="No video in playlist :(", bootstyle="danger").pack(side="top", padx=10, pady=10)
        else:
            self.which_tab = 0
            self.playlist_tab.configure(bootstyle="danger")
            self.all_video_clicked()

    def add_play_list(self, id):
        AddToPlaylist(tk.Toplevel(), id)

    def deletet_playlist(self, id, is_playlist=0, playlist_name=""): 
        db.playlist[playlist_name][id] = 0
        db.save_data()
        if is_playlist:
            self.open_playlist(1)
            return
        self.all_video_clicked()

    def add_new_playlist(self):
        self.clear_frame()
        self.addPlaylistButton.configure(bootstyle="light")
        # Instruction Label
        label = tb.Label(self.videoList, text="Enter the name of the new playlist:", bootstyle="danger")
        label.pack(side="top", padx=10, pady=10)

        # Entry for new playlist name
        new_playlist_name = tb.Entry(self.videoList, bootstyle="danger", width=30)
        new_playlist_name.pack(side="top", padx=10, pady=10)

        # Frame for buttons
        button_frame = tb.Frame(self.videoList, bootstyle="default")
        button_frame.pack(side="top", padx=10, pady=10)

        # Add Button with Icon
        add_button = tb.Button(button_frame, text="➕ Add", bootstyle="success", compound="left",
                               command=lambda: self.add_playlist_name(new_playlist_name.get()))
        add_button.pack(side="left", padx=10)

        # Quit Button with Icon
        quit_button = tb.Button(button_frame, text="❌ Quit", bootstyle="danger", compound="left",
                                command=self.all_video_clicked)
        quit_button.pack(side="left", padx=10)

    def add_playlist_name(self, new_playlist_name):
        if new_playlist_name == "":
            return
        if new_playlist_name in db.playlist_name:
            return
        db.playlist_name.append(new_playlist_name)
        db.playlist[new_playlist_name] = [0] * (lib.max_id + 1)
        db.save_data()
        self.playlist_tab["value"] = db.playlist_name
        self.all_video_clicked()
    def delete_playlist_name(self, playlist_name):
        if playlist_name == "":
            return
            
        if playlist_name not in db.playlist_name:
            return
        db.playlist_name.remove(playlist_name)
        db.playlist.pop(playlist_name)
        self.all_video_clicked()
        db.save_data()

    # end for playlist

    def search_video_click(self):
        self.clear_frame()
        self.which_tab = 2
        ok = False
        self.addPlaylistButton.configure(bootstyle="danger")
        search_type = self.selectSearchType.get()
        result = []
        # add back button
        backButton = tb.Button(self.videoList, text="Back", bootstyle="danger", command=self.back_button_clicked_for_search)
        backButton.pack(side="top", padx=10, pady=10)
        if search_type == "Video ID":
            id = self.searchBar.get()
            if not self.check_integer(id):
                ok = False
            else:
                id = int(id)
                if id in lib.library:
                    result.append(id)
                    ok = True
        elif search_type == "Title":
            title = self.searchBar.get()
            for object in lib.library:
                if title.lower() in lib.library[object].name.lower():
                    ok = True
                    result.append(object)
        elif search_type == "Director":
            director = self.searchBar.get()
            for object in lib.library:
                if director.lower() in lib.library[object].director.lower():
                    ok = True
                    result.append(object)
        if ok:
            for object in result:
                id = object
                videoname = lib.library[object].name
                rating = lib.library[object].rating
                tag = lib.library[object].tag
                length = lib.library[object].length
                year = lib.library[object].year
                director = lib.library[object].director
                videoIdInformation = f"     {id}.  "
                videoYearTimeInformation = f"     {year}  {math.floor(length/60)}h {length%60}m  {tag} \n    Director: {director}"
                videoRatingInformation = f"★{rating}"
                # Create frames for video information
                self.videoFrameTop = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                self.videoFrameTop.pack(side="top", padx=10, pady=10, fill="x")  # Pack at the top with horizontal padding 10, vertical padding 10, filling horizontally
                videoYearTimeInformation = f"     {year}  {math.floor(length/60)}h {length%60}m  {tag}"
                videoRatingInformation = f"★{rating}"
                # Labels displaying video information
                tb.Label(self.videoFrameTop, text=videoIdInformation, bootstyle="default", justify="left").pack(side="left")  # Pack on the left with left justification
                tb.Label(self.videoFrameTop, text=videoname, bootstyle="default").pack(side="left", padx=0)  # Pack on the left with no horizontal padding
                self.videoFrameMiddle = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                self.videoFrameMiddle.pack(side="top", padx=10, fill="x")  # Pack at the top with horizontal padding 10, filling horizontally
                tb.Label(self.videoFrameMiddle, text=videoYearTimeInformation, bootstyle="default").pack(side="left")  # Pack on the left
                self.videoFrameBottom = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                self.videoFrameBottom.pack(side="top", padx=10, fill="x")  # Pack at the top with horizontal padding 10, filling horizontally
                tb.Label(self.videoFrameBottom, text=videoRatingInformation, bootstyle="default").pack(side="left", padx=60)  # Pack on the left with horizontal padding 60
                
                # Buttons and separators
            
                tb.Button(self.videoFrameMiddle, text="➕", bootstyle="link", command=lambda id=id: self.add_play_list(id)).pack(side="right", padx=40)  # Create a button with link bootstyle and a command callback, pack on the right with horizontal padding 40
                tb.Separator(self.videoFrameMiddle, bootstyle="Active")  # Create a frame with Active bootstyle", orient="vertical").pack(side="right", fill="y")  # Create a vertical separator with Active")  # Create a frame with Active bootstyle bootstyle, pack on the right filling vertically
                self.infoButton = tb.Button(self.videoFrameMiddle, text="ℹ️", bootstyle="link", command=lambda id=id: self.video_info_and_rate_click(id, 2))  # Create a button with link bootstyle and a command callback
                self.infoButton.pack(side="right", padx=40)  # Pack on the right with horizontal padding 40
                self.rateStar = tb.Button(self.videoFrameBottom, text="☆ rate", bootstyle="link", command=lambda id=id: self.video_info_and_rate_click(id, 2))  # Create a button with link bootstyle and a command callback
                self.rateStar.pack(side="left", padx=10)  # Pack on the left with horizontal padding 10
                # Line separator
                self.lineFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a default-themed frame
                self.lineFrame.pack(side="top", fill="x", pady=20)  # Pack at the top filling horizontally, with vertical padding 20
                tb.Separator(self.lineFrame, bootstyle="light", orient="horizontal").pack(side="bottom", fill="x", padx=20)  # Create a horizontal separator with light bootstyle, pack at the bottom filling horizontally, with horizontal padding 20
        else:
            tb.Label(self.videoList, text="No result found :(", bootstyle="danger").pack(side="top", padx=10, pady=10)

    def video_info_and_rate_click(self, id, previous_tab=0):  # previous_tab = 0 is in the video list tab, 1 is in the playlist tab, 2 is in the search tab
        self.clear_frame()
        self.which_tab = 3

        # Add back button
        backButton = tb.Button(self.videoList, text="Back", bootstyle="danger", command=lambda: self.back_button_clicked(previous_tab))
        backButton.pack(side="top", padx=10, pady=10)
        # Add play button
        playButton = tb.Button(self.videoList, text="Play", bootstyle="danger", command=lambda: self.play_video(id, previous_tab))
        playButton.pack(side="top", padx=10, pady=10)

        # Retrieve video details
        videoname = lib.library[id].name
        rating = lib.library[id].rating
        tag = lib.library[id].tag
        videoDirector = lib.library[id].director
        length = lib.library[id].length
        year = lib.library[id].year
        playcount = lib.library[id].play_count

        # Create frames for different sections of video information
        videoImageFrame = tb.Label(self.videoList, bootstyle="default")  # Create a video image frame with default bootstyle
        videoImageFrame.pack(side="top", padx=40, pady=20)  # Pack at the left of the window with padding

        videoTitleFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a Frame to display video Title
        videoTitleFrame.pack(side="top", fill="x", padx=40)  # Pack at the top of the window with padding

        videoInfoFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a video information frame
        videoInfoFrame.pack(side="top", fill="x", padx=40, pady=10)  # Pack below the video title frame with padding

        videoDirectorFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a frame to display the director name
        videoDirectorFrame.pack(side="top", fill="x", padx=40, pady=10)  # Pack below the video information frame with padding

        videoDescriptionFrame = tb.Frame(self.videoList, bootstyle="default")  # Create a video description frame with default bootstyle
        videoDescriptionFrame.pack(side="bottom", fill="x", padx=40, pady=20)  # Pack at the bottom of the window with padding

        descriptionSep = tb.Separator(self.videoList, bootstyle="light")  # Create a separator line between video description and video info frame
        descriptionSep.pack(side="bottom", fill="x", padx=20)  # Pack above the video description frame

        # Labels displaying video information in different frames
        videoTitle = tb.Label(videoTitleFrame, bootstyle="default", text=f"{id}. {videoname}")
        videoTitle.pack(side="left", padx=0)  # Pack the video title inside the videoTitleFrame on the left

        videoInfo = tb.Label(videoInfoFrame, bootstyle="default", text=f"Year: {year} || Length: {math.floor(length/60)}h {length%60}m \nType: {tag} || Rate: {rating} ☆ || Watched: {playcount}")
        videoInfo.pack(side="left", padx=0)  # Pack the video information inside the videoInfoFrame on the left

        videoDirector = tb.Label(videoDirectorFrame, bootstyle="default", text=f"Director: {videoDirector}")
        videoDirector.pack(side="left", padx=0)  # Pack the director name inside the videoDirectorFrame on the left

        videodescription = lib.library[id].description
        videoDescription = tb.Label(videoDescriptionFrame, bootstyle="default", text=videodescription, wraplength=1300)
        videoDescription.pack(side="left", padx=0)  # Pack the video description inside the videoDescriptionFrame on the left

        # Frame for rate stars
        self.rateFrame = tb.Frame(self.videoList, bootstyle="default")
        self.rateFrame.pack(side="top", padx=10, pady=10)
        
        # Create star buttons
        self.stars = []
        for i in range(1, 6):
            star_button = tb.Button(self.rateFrame, text="☆", bootstyle=self.bootstyleNotChoose, command=lambda i=i: self.rate_video(id, i))
            star_button.pack(side="left", padx=3)
            self.stars.append(star_button)
        
        self.update_star_buttons(db.user_rate[id])

        try:
            # Attempt to open an image file corresponding to the video's ID and resize it
            image_original = Image.open(f"./images/{id}.jpg").resize((300, 450))
        except:
            # Use a default "no picture available" image and resize it
            image_original = Image.open(f"./images/no.png").resize((300, 450))  # Use the no picture available picture instead

        # Convert the original image to a PhotoImage object compatible with Tkinter
        image_tk = ImageTk.PhotoImage(image_original)
        videoImageFrame.configure(image=image_tk)
        videoImageFrame.image = image_tk

    def rate_video(self, id, rating):
        new_rating = rating
        # check the rating is >= 1 and <= 5
        # update the new_rating
        if db.user_rate[id] != 0:
            lib.new_rating_update(id, new_rating)
            db.user_rate[id] = new_rating
        else:
            lib.library[id].total_of_rating -= db.user_rate[id]
            lib.library[id].total_of_rating += new_rating
            db.user_rate[id] = new_rating            
            lib.library[id].rating = lib.library[id].total_of_rating / lib.library[id].number_of_rate_time
        db.save_data()
        lib.save_data()
        self.update_star_buttons(rating)
        self.video_info_and_rate_click(id)

    def update_star_buttons(self, rating):
        for i in range(5):
            if i < rating:
                self.stars[i].configure(bootstyle=self.bootstyleChoose)
            else:
                self.stars[i].configure(bootstyle=self.bootstyleNotChoose)

    def back_button_clicked_for_search(self):
        self.all_video_clicked()
        self.which_tab = 0
        self.searchBar.delete(0, 'end')  # Clear the search bar
        self.selectSearchType.current(0)  # Reset the combobox to the first option

    def play_video(self, id, previous_tab=0):
        lib.library[id].play_count += 1
        lib.save_data()
        self.clear_frame()
        self.video_info_and_rate_click(id, previous_tab)

    def back_button_clicked(self, previous_tab=0):
        self.clear_frame()
        if previous_tab == 0:
            self.all_video_clicked()
        elif previous_tab == 1:
            self.open_playlist(1)
        elif previous_tab == 2:
            self.search_video_click()

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = VideoPlayer(root)
    root.mainloop()
