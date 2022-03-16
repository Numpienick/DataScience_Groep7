import re
import csv

from Regex import *


def readFile(dataType):
    print("\nStarts reading " + dataType.file)
    try:
        with open("data/" + dataType.file + ".list", "r", encoding="ANSI") as f:
            txt = f.read()
            data = re.findall(dataType.regex, str(txt))
            print("Done reading " + dataType.file)
            return data
    except IOError:
        print("File could not be opened: " + dataType.file)


def writeCSV(data, name):
    print("\nStarts writing " + name)
    try:
        with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
            writer = csv.writer(f, delimiter=';', dialect="excel")
            writer.writerows(data)
            print("Done writing to " + name + ".csv")
    except IOError:
        print("File could not be created: " + name + ".csv")


print("Welkom bij de IMDB-Parser van groep 7")
print("Welke dataset wil je omzetten naar CSV?")
print(
    "1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movie \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal")

dataSetChoice = int(input())

if dataSetChoice == 1 or dataSetChoice == 0:
    actor = Actor()
    writeCSV(readFile(actor), actor.file)
if dataSetChoice == 2 or dataSetChoice == 0:
    actress = Actress()
    writeCSV(readFile(actress), actress.file)
if dataSetChoice == 3 or dataSetChoice == 0:
    cinematographer = Cinematographer()
    writeCSV(readFile(cinematographer), cinematographer.file)
if dataSetChoice == 4 or dataSetChoice == 0:
    country = Country()
    writeCSV(readFile(country), country.file)
if dataSetChoice == 5 or dataSetChoice == 0:
    director = Director()
    writeCSV(readFile(director), director.file)
if dataSetChoice == 6 or dataSetChoice == 0:
    genre = Genre()
    writeCSV(readFile(genre), genre.file)
if dataSetChoice == 7 or dataSetChoice == 0:
    movie = Movie()
    writeCSV(readFile(movie), movie.file)
if dataSetChoice == 8 or dataSetChoice == 0:
    plot = Plot()
    writeCSV(readFile(plot), plot.file)
if dataSetChoice == 9 or dataSetChoice == 0:
    rating = Rating()
    writeCSV(readFile(rating), rating.file)
if dataSetChoice == 10 or dataSetChoice == 0:
    runningTime = RunningTime()
    writeCSV(readFile(runningTime), runningTime.file)

print("Done!")
