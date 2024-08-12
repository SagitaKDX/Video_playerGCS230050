from library_item import LibraryItem

import pandas as pd
import csv


max_id = 0
library = {}
csvfile = open('Corrected_Movie_Data.csv', newline='')
c = csv.reader(csvfile)
ok = False
for row in c:
    if(row[0] == ""):
        break
    content = ""
    with open(f"videoinfo/{int(row[0])}.txt", 'r') as file:
        content = file.read()
    description = content
    library[int(row[0])] = LibraryItem(row[1], row[2], int(row[3]), int(row[4]), int(row[5]) , int(row[6]) , row[7] , row[8] , int(row[9]) , int(row[10]) , description)
    max_id = max(max_id, int(row[0]))
csvfile.close()

def save_data():
    with open('Corrected_Movie_Data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key in library:
            item = library[key]
            writer.writerow([key, item.name, item.director, item.rating, item.number_of_rate_time, item.total_of_rating , item.play_count , item.tag , item.type , item.length , item.year])    

def list_all():
    output = ""
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output


def get_name(key):
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None


def get_director(key):
    try:
        item = library[key]
        return item.director
    except KeyError:
        return None


def get_rating(key):
    try:
        item = library[key]
        return int(round(item.rating))
    except KeyError:
        return -1


def set_rating(key, rating):
    try:
        item = library[key]
        item.rating = rating
    except KeyError:
        return


def get_play_count(key):
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1


def increment_play_count(key):
    try:
        item = library[key]
        item.play_count += 1
    except KeyError:
        return
def new_rating_update(key , value):
    try:
        item = library[key]
        item.number_of_rate_time += 1
        item.total_of_rating += value
        item.rating = round(item.total_of_rating / item.number_of_rate_time)
    except KeyError:
        return -1