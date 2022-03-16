import re
import csv

from DbConnector import connect
from Regex import *


def readFile(dataType):
    file = open("data/" + dataType.file + ".list", "r", encoding="ANSI")
    txt = file.read()
    data = re.findall(dataType.initialRegex, str(txt))
    print("done reading")
    file.close()
    return data

def getMatches(dataType):
    file = open("data/" + dataType.file + ".list", "r", encoding="ANSI")
    lines = file.readlines()
    matches = list()
    for line in lines:
        match = re.search(dataType.regex, line, re.M)
        if match is not None:
            matches.append(match)
    return matches


def writeCSV(data, name):
    # create the csv writer
    with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
        writer = csv.writer(f, delimiter=';', dialect="excel")
        writer.writerows(data)
    print("done writing to CSV")


# Movies
movie = Movie()
#matches = getMatches(movie)

# Country
country = Country()
# writeCSV(readFile(country), country.file)

# Plot
plot = Plot()
# writeCSV(readFile(plot), plot.file)

rating = Rating()
#writeCSV(readFile(rating), rating.file)
