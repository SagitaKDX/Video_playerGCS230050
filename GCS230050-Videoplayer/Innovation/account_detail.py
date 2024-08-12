import video_library as lib
import csv
import os
class account():
    def __init__(self):
        self.user_name = ""
        self.first_time = True
        self.user_rate = []
        self.rows = []
        self.playlist_name = []
        self.playlist = {}
    def load_data(self):
        if self.first_time:
            self.user_rate = [0 for i in range(0, lib.max_id + 1)]
            self.playlist["Playlist"] =  [0 for i in range(0 , lib.max_id + 1)]
            self.playlist_name = ["Playlist"]
        else:
            folder_path = os.path.join(os.path.dirname(__file__), "user_data")
            file_name = f"{self.user_name}.csv"
            file_path = os.path.join(folder_path, file_name)
            # 0 la ban dau
            # 1 la theo id
            self.user_rate = []
            self.rows = []
            self.playlist_name = []
            self.playlist = {}
            with open(file_path, newline='') as csvfile:
                c = csv.reader(csvfile)
                self.rows = list(c)
                idx = 0
                for row in self.rows:
                    if row[0] == "":
                        break
                    idx += 1
                    if(idx == 1):
                        collumn = 0
                        for each in row:
                            if(each == ""):
                                break
                            if(collumn == 0):
                                self.user_rate.append(0)
                                collumn += 1
                                continue
                            self.playlist[each] = [0]
                            self.playlist_name.append(each)
                            collumn += 1
                    else: 
                        self.user_rate.append(int(row[0]))
                        for i in range(1 , len(row)):
                            self.playlist[self.playlist_name[i - 1]].append(int(row[i]))
            #self.playlist name start from 0 , self.playlist start from 1
            csvfile.close()
            if(idx + 1 < lib.max_id):
                self.user_rate += [0 for i in range(idx + 1 , lib.max_id + 1)]

    def save_data(self):
        folder_path = os.path.join(os.path.dirname(__file__), "user_data")
        file_name = f"{self.user_name}.csv"
        idx = 0
        if(self.first_time):
            #create new file
            with open (os.path.join(folder_path, file_name), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(0 , len(self.user_rate)):
                    idx += 1
                    if(idx == 1):
                        writer.writerow([self.user_rate[i]] + self.playlist_name)
                        continue
                    row = [self.user_rate[i]]
                    for name in self.playlist_name:
                        row.append(self.playlist[name][i])  
                    writer.writerow(row)
            csvfile.close()
        else:
            #over write the data
             
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w' , newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(0 , len(self.user_rate)):
                    idx += 1
                    if(idx == 1):
                        writer.writerow([self.user_rate[i]] + self.playlist_name)
                        continue
                    row = [self.user_rate[i]]
                    for name in self.playlist_name:
                        row.append(self.playlist[name][i])  
                    writer.writerow(row)
            csvfile.close()


db = account()