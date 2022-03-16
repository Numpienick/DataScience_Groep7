import re
import csv

from Regex import *


def readFile(dataType):
    with open("data/" + dataType.file + ".list", "r", encoding="ANSI") as f:
        txt = f.read()
        data = re.findall(dataType.regex, str(txt))
        print("done reading " + dataType.file)
        return data


def writeCSV(data, name):
    # create the csv writer
    with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
        writer = csv.writer(f, delimiter=';', dialect="excel")
        writer.writerows(data)
        print("done writing to " + name + ".csv")


# Movies
movie = Movie()
# writeCSV(readFile(movie), movie.file)

# Country
country = Country()
# writeCSV(readFile(country), country.file)

# Plot
plot = Plot()
# writeCSV(readFile(plot), plot.file)

rating = Rating()
# writeCSV(readFile(rating), rating.file)

actress = Actress()
# writeCSV(readFile(actress), actress.file)

actor = Actor()
# writeCSV(readFile(actor), actor.file)

cinematographer = Cinematographer()
# writeCSV(readFile(cinematographer), cinematographer.file)

director = Director()
writeCSV(readFile(director), director.file)