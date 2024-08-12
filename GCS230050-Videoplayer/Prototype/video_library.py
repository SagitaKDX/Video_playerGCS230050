from library_item import LibraryItem

import pandas as pd
import csv


max_id = 0
library = {}
csvfile = open('data.csv', newline='')
c = csv.reader(csvfile)
for row in c:
    if(row[0] == ""):
        break
    library[int(row[0])] = LibraryItem(row[1], row[2], int(row[3]), int(row[4]), int(row[5]) , int(row[6]))
    max_id = max(max_id, int(row[0]))
csvfile.close()

def save_data():
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key in library:
            item = library[key]
            writer.writerow([key, item.name, item.director, item.rating, item.number_of_rate_time, item.total_of_rating , item.play_count])

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