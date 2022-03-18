import re
import csv
import time
import itertools as it

from DbConnector import connect
from Regex import *


def readFile(dataType):
    print(f"\nStarts reading {dataType.file}")
    startTime = time.perf_counter()
    try:
        with open("data/" + dataType.file + ".list", "r", encoding="ANSI") as f:
            data = dataType.sectionData(f)
            if data != "":
                data = re.findall(dataType.regex, data)
                return data
            txt = f.read()
            cleanfileRegex = dataType.cleanFileRegex
            if cleanfileRegex != r"":
                cleaned = re.search(cleanfileRegex, str(txt))
                dataStr = str(cleaned.group("data"))
                data = re.findall(dataType.regex, dataStr)
                endTime = time.perf_counter()
                print(f"Done reading {dataType.file} in {endTime - startTime:0.04f} seconds")
                return data
            data = re.findall(dataType.regex, str(txt))
            endTime = time.perf_counter()
            print(f"Done reading {dataType.file} in {endTime - startTime:0.04f} seconds")
            return data
    except Exception as e:
        print(e)


def getMatches(dataType):
    print(f"\nStarts getting matches from {dataType.file}")
    startTime = time.perf_counter()
    try:
        with open("data/" + dataType.file + ".list", "r", encoding="ANSI") as f:
            cleanfileRegex = dataType.cleanFileRegex
            if cleanfileRegex != r"":
                cleaned = re.search(cleanfileRegex, str(txt))
                dataStr = str(cleaned.group("data"))
                lines = dataStr.splitlines()
            else:
                lines = f.readlines()
            matches = list()
            for line in lines:
                match = re.search(dataType.regex, line, re.M)
                if match is not None:
                    matches.append(match)
            endTime = time.perf_counter()
            print(f"Done getting matches from {dataType.file} in {endTime - startTime:0.04f} seconds")
            return matches
    except Exception as e:
        print(e)


def writeCSV(data, dataType):
    startTime = time.perf_counter()
    name = dataType.file
    pattern = re.compile(dataType.regex)
    groups = str(pattern.groupindex)
    headers = re.findall(r"([a-z]+)", groups, re.M | re.I)
    print(f"\nStarts writing {name}")
    try:
        with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
            writer = csv.writer(f, delimiter=';', dialect="excel")
            writer.writerow(headers)
            writer.writerows(data)
            endTime = time.perf_counter()
            print(f"Done writing to {name}.csv in {endTime - startTime:0.04f} seconds")
    except Exception as e:
        print(e)


def main():
    print("Welkom bij de IMDB-Parser van groep 7")
    print("Welke dataset wil je omzetten naar CSV?")
    print(
        "1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movie \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal")

    dataSetChoice = input()
    startTime = time.perf_counter()

    match(dataSetChoice):
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
    endTime = time.perf_counter()
    print(f"\nFinished parsing in {endTime - startTime:0.04f} seconds")


main()
