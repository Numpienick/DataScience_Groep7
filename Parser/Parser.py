import re
import csv

from DbConnector import connect
from Regex import *


def readFile(dataType):
    file = open("data/" + dataType.file + ".list", "r", encoding="ANSI")
    txt = file.read()
    data = re.findall(dataType.regex, str(txt))
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


def writeCSV(data, dataType):
    pattern = re.compile(dataType.regex)
    groups = str(pattern.groupindex)
    headers = re.findall(r"([a-z]+)", groups, re.M | re.I)
    # create the csv writer
    with open("output/" + dataType.file + '.csv', 'w', encoding="ANSI", newline='') as f:
        writer = csv.writer(f, delimiter=';', dialect="excel")
        writer.writerow(headers)
        writer.writerows(data)
    print("done writing to CSV")


# Movies
movie = Movie()
#matches = getMatches(movie)
writeCSV(readFile(movie), movie)

# Country
country = Country()
# writeCSV(readFile(country), country.file)

# Plot
plot = Plot()
# writeCSV(readFile(plot), plot.file)

rating = Rating()
#writeCSV(readFile(rating), rating.file)
