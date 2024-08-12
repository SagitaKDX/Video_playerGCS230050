import video_library as lib
import csv
import os
class account():
    def __init__(self):
        self.user_name = ""
        self.first_time = True
        self.user_rate = []
        self.user_comment = []
        self.rows = []
        self.playlist = []
    def load_data(self):
        if self.first_time:
            self.user_rate = [0 for i in range(0, lib.max_id + 1)]
            self.playlist =  [0 for i in range(0 , lib.max_id + 1)]
        else:
            folder_path = os.path.join(os.path.dirname(__file__), "user_data")
            file_name = f"{self.user_name}.csv"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, newline='') as csvfile:
                c = csv.reader(csvfile)
                self.rows = list(c)
                idx = 0
                for row in self.rows:
                    if row[0] == "":
                        break
                    idx += 1
                    if(idx == 1):
                        self.user_rate.append(0)
                        self.playlist.append(0)
                    else: 
                        self.user_rate.append(int(row[0]))
                        self.playlist.append(int(row[1]))
            csvfile.close()
            if(idx + 1 < lib.max_id):
                self.user_rate += [0 for i in range(idx + 1 , lib.max_id + 1)]

    def save_data(self):
        folder_path = os.path.join(os.path.dirname(__file__), "user_data")
        file_name = f"{self.user_name}.csv"
        if(self.first_time):
            with open (os.path.join(folder_path, file_name), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(0 , len(self.user_rate)):
                    writer.writerow([self.user_rate[i] , self.playlist[i]])
            csvfile.close()
        else:
            #over write the data
             
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w' , newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(0 , len(self.user_rate)):
                    writer.writerow([self.user_rate[i] , self.playlist[i]])
            csvfile.close()


db = account()