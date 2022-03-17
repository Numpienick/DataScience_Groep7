import re
import csv

from DbConnector import connect
from Regex import *


# Reads .list file
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

        
# Gets matches based on header
def getMatches(dataType):
    file = open("data/" + dataType.file + ".list", "r", encoding="ANSI")
    lines = file.readlines()
    matches = list()
    for line in lines:
        match = re.search(dataType.regex, line, re.M)
        if match is not None:
            matches.append(match)
    file.close()
    return matches


# Writes CSV with data from .list file
def writeCSV(data, dataType):
    name = dataType.file
    pattern = re.compile(dataType.regex)
    groups = str(pattern.groupindex)
    headers = re.findall(r"([a-z]+)", groups, re.M | re.I)
    print("\nStarts writing " + name)
    try:
        with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
            writer = csv.writer(f, delimiter=';', dialect="excel")
            writer.writerow(headers)
            writer.writerows(data)
            print("Done writing to " + name + ".csv")
    except IOError:
        print("File could not be created: " + name + ".csv")


def main():
    print("Welkom bij de IMDB-Parser van groep 7")
    print("Welke dataset wil je omzetten naar CSV?")
    print("1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movie \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal")

    dataSetChoice = input()

    match (dataSetChoice):
        case "0":
            data = Actor()
            writeCSV(readFile(data), data)
            data = Actress()
            writeCSV(readFile(data), data)
            data = Cinematographer()
            writeCSV(readFile(data), data)
            data = Country()
            writeCSV(readFile(data), data)
            data = Director()
            writeCSV(readFile(data), data)
            data = Genre()
            writeCSV(readFile(data), data)
            data = Movie()
            writeCSV(readFile(data), data)
            data = Plot()
            writeCSV(readFile(data), data)
            data = Rating()
            writeCSV(readFile(data), data)
            data = RunningTime()
            writeCSV(readFile(data), data)
        case "1":
            actor = Actor()
            writeCSV(readFile(actor), actor)
        case "2":
            actress = Actress()
            writeCSV(readFile(actress), actress)
        case "3":
            cinematographer = Cinematographer()
            writeCSV(readFile(cinematographer), cinematographer)
        case "4":
            country = Country()
            writeCSV(readFile(country), country)
        case "5":
            director = Director()
            writeCSV(readFile(director), director)
        case "6":
            genre = Genre()
            writeCSV(readFile(genre), genre)
        case "7":
            movie = Movie()
            writeCSV(readFile(movie), movie)
        case "8":
            plot = Plot()
            writeCSV(readFile(plot), plot)
        case "9":
            rating = Rating()
            writeCSV(readFile(rating), rating)
        case "10":
            runningTime = RunningTime()
            writeCSV(readFile(runningTime), runningTime)
        case _:
            print("\n" * 100)
            print("Dat is geen optie. Probeer het opnieuw\n\n")
            main()


main()
print("Done!")