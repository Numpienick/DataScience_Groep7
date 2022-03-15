import re
import csv

# actorsList = open("data/movies.list", "r", encoding="ANSI")
# print(actorsList.read())

#Movies
from Regex import *

movie = Movie()
file = open("data/"+movie.file+".list", "r", encoding="ANSI")
txt = file.read()
movies = re.split(movie.initialRegex, str(txt))

#opens file, writes every element of array with \n between
# with open("text.txt", 'w') as file:
#     file.write('\n'.join(x))

with open('text.csv', 'w') as f:
    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(movies)
    # for i in x:
    #     # write a row to the csv file
    #     writer.writerow(i)
    #     print(i)
print("done")

file.close()

#Actors
