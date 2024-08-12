from library_item import LibraryItem

class ItemEpisode(LibraryItem):
    def __init__(self, title, director, episode_year, episode_number, episode_length, episode_rating):
        LibraryItem.__init__(title, director)
        self.episode_year = episode_year
        self.episode_number = episode_number
        self.episode_length = episode_length
        self.episode_rating = episode_rating
        self.episode_playcount = 0
    def info(self):
        return self.title, self.director, self.episode_year, self.episode_number, self.episode_length, self.episode_rating, self.episode_playcount