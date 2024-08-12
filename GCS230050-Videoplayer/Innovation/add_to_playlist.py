from tkinter import *  # Import all from tkinter
import ttkbootstrap as tb  # Import ttkbootstrap library as tb
from ttkbootstrap.scrolled import ScrolledFrame  # Import ScrolledFrame from ttkbootstrap.scrolled
import font_manager as fonts  # Import font_manager file as fonts
from video_library import *  # Import all from video_library file
from account_detail import db  # Import db from account_detail


class AddToPlaylist:
    def __init__(self, window, video_id):
        self.window = window
        self.video_id = video_id
        self.setup_ui()

    def setup_ui(self):
        self.window.geometry("550x400")
        fonts.configure()
        self.window.title("Add to Playlist")

        # Title Label
        tb.Label(self.window, text="Add to Playlist", font=("Times New Roman", 16, "bold")).pack(side="top", pady=20)

        # Top Frame
        self.topFrame = tb.Frame(self.window, bootstyle="default")
        self.topFrame.pack(side="top", fill="x", padx=20, pady=20)

        # Separator
        self.labelSep = tb.Separator(self.window, bootstyle="light", orient="horizontal")
        self.labelSep.pack(side="top", pady=0, fill="x")

        # Scrolled Frame for Playlist
        self.playlistFrame = ScrolledFrame(self.window, bootstyle="default")
        self.playlistFrame.pack(side="top", fill="both", padx=20, expand=YES)

        # Load Playlists
        self.load_playlist()

    def clear_frame(self):
        for widget in self.playlistFrame.winfo_children():
            widget.destroy()

    def load_playlist(self):
        self.clear_frame()
        for name in db.playlist_name:
            playlist_frame = tb.Frame(self.playlistFrame, bootstyle="default")
            playlist_frame.pack(side="top", fill="x", padx=20, pady=10)

            playlist_name_label = tb.Label(playlist_frame, text=name, bootstyle="default")
            playlist_name_label.pack(side="left", pady=10)

            # Add/Remove button
            is_in_playlist = db.playlist[name][self.video_id] == 1
            button_text = "❌" if is_in_playlist else "➕"
            button_command = (lambda n=name: self.delete_from_playlist(n, self.video_id)) if is_in_playlist else (lambda n=name: self.add_to_playlist(n, self.video_id))

            button = tb.Button(playlist_frame, text=button_text, command=button_command, bootstyle="default")
            button.pack(side="right", pady=10)

    def add_to_playlist(self, playlist_name, video_id):
        db.playlist[playlist_name][video_id] = 1
        db.save_data()
        self.load_playlist()

    def delete_from_playlist(self, playlist_name, video_id):
        db.playlist[playlist_name][video_id] = 0
        db.save_data()
        self.load_playlist()


# Example usage:
if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = AddToPlaylist(root, video_id="example_video_id")
    root.mainloop()
