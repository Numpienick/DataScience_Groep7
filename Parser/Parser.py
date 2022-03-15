import re
import csv

from Regex import *


def readFile(dataType):
    file = open("data/" + dataType.file + ".list", "r", encoding="ANSI")
    txt = file.read()
    data = re.findall(dataType.initialRegex, str(txt))
    print("done reading")
    file.close()
    return data


def writeCSV(data, name):
    # create the csv writer
    with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
        writer = csv.writer(f, delimiter=';', dialect="excel")
        writer.writerows(data)
    print("done writing to CSV")


# Movies
movie = Movie()
writeCSV(readFile(movie), movie.file)

# Country
country = Country()
# writeCSV(readFile(country), country.file)

# Plot
plot = Plot()
# writeCSV(readFile(plot), plot.file)

rating = Rating()
writeCSV(readFile(rating), rating.file)
