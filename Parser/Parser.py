import re
import csv

from Regex import *

def readFile(dataType):
    file = open("data/" + dataType.file + ".list", "r", encoding="ANSI")
    txt = file.read()
    data = re.split(dataType.initialRegex, str(txt))
    print("done reading")
    file.close()
    return data

def writeCSV(data, name):
    with open("output/" + name + '.csv', 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(data)
    print("done writing to CSV")

#Movies
movie = Movie()
writeCSV(readFile(movie), movie.file)

#Country
country = Country()
writeCSV(readFile(country), country.file)
