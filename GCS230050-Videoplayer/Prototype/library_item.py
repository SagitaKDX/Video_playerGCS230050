class LibraryItem:
    def __init__(self, name, director, rating=0 , number_of_rate_time = 0 , total_of_rating = 0 , play_count = 0):
        self.name = name
        self.director = director
        self.rating = rating
        self.play_count = play_count
        self.number_of_rate_time = number_of_rate_time
        self.total_of_rating = total_of_rating


    def info(self):
        return f"{self.name} - {self.director} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.rating):
            stars += "*"
        return stars
