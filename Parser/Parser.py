import re
import csv
import time
import itertools as it

from DbConnector import *
from DbConverter import *
from Regex import *


# Reads IMDB .list file
def read_file(data_type):
    print(f"\nStarts reading {data_type.file}")
    startTime = time.perf_counter()
    try:
        with open("data/" + data_type.file + ".list", "r", encoding="ANSI") as f:
            data = data_type.sectionData(f)
            if data != "":
                data = re.findall(data_type.regex, data)
                return data
            txt = f.read()
            txt = re.sub(';', ':', txt)
            txt = re.sub('\\\\', ' ', txt)

            # Some files needs a cleanup step before the regex, this if statement will trigger
            if len(data_type.cleanFileRegex.strip()) > 0:
                print(f"\nStarts cleaning {data_type.file}")
                cleaned = re.search(data_type.cleanFileRegex, str(txt))
                txt = str(cleaned.group("data"))
                end_time_clean = time.perf_counter()
                print(f"Done cleaning {data_type.file} in {end_time_clean - startTime:0.04f} seconds")
                print(f"\nContinuing reading {data_type.file}")

            data = re.findall(data_type.regex, str(txt))
            end_time = time.perf_counter()
            print(f"Done reading {data_type.file} in {end_time - startTime:0.04f} seconds")
            return data
    except Exception as e:
        print(e)


# Can loop through regexxed data line by line
# At the moment unused
def get_matches(data_type):
    print(f"\nStarts getting matches from {data_type.file}")
    start_time = time.perf_counter()
    try:
        with open("data/" + data_type.file + ".list", "r", encoding="ANSI") as f:
            txt = f.read()
            cleanfile_regex = data_type.cleanFileRegex
            if cleanfile_regex != r"":
                cleaned = re.search(cleanfile_regex, str(txt))
                dataStr = str(cleaned.group("data"))
                lines = dataStr.splitlines()
            else:
                lines = f.readlines()
            matches = list()
            for line in lines:
                match = re.search(data_type.regex, line, re.M)
                if match is not None:
                    matches.append(match)
            end_time = time.perf_counter()
            print(f"Done getting matches from {data_type.file} in {end_time - start_time:0.04f} seconds")
            return matches
    except Exception as e:
        print(e)


# Writes csv from read file
def write_csv(data, data_type):
    start_time = time.perf_counter()
    name = data_type.file
    pattern = re.compile(data_type.regex)
    groups = str(pattern.groupindex)
    headers = re.findall(r"([_a-z]+)", groups, re.M | re.I)
    print(f"\nStarts writing {name}")

    try:
        with open("output/" + name + '.csv', 'w', encoding="ANSI", newline='') as f:
            writer = csv.writer(f, dialect="excel", delimiter=';', quoting=csv.QUOTE_MINIMAL)

            # Adds female header to actors/actresses
            if name == "actors" or name == "actresses":
                list_headers = list(headers)
                list_headers.insert(22, 'female')
                writer.writerow(tuple(list_headers))
            else:
                writer.writerow(headers)

            # With persons loops through every row, if all names are empty, uses the last filled one to fill it.
            if name == "actors" or name == "actresses" or name == "cinematographers" or name == "directors":
                for line in data:
                    listed = list(line)
                    if name == "actors":
                        listed.insert(22, 0)
                    if name == "actresses":
                        listed.insert(22, 1)
                    if line[0] == '' and line[1] == '' and line[2] == '':
                        listed[0] = old_nickname
                        listed[1] = old_lastname
                        listed[2] = old_firstname
                        tuple_line = tuple(listed)
                    else:
                        old_nickname = line[0]
                        old_lastname = line[1]
                        old_firstname = line[2]
                        tuple_line = tuple(listed)
                    writer.writerow(tuple_line)
            else:
                writer.writerows(data)
            end_time = time.perf_counter()
            print(f"Done writing to {name}.csv in {end_time - start_time:0.04f} seconds")
    except Exception as e:
        print(e)


# Main function, provides info and choice
def main():
    print("Welkom bij de IMDB-Parser van groep 7")
    print("Welke dataset wil je omzetten naar CSV?")
    print(
        "1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movie \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal")

    data_set_choice = input()
    start_time = time.perf_counter()

    match data_set_choice:
        case "0":
            data = Actor()
            write_csv(read_file(data), data)
            data = Actress()
            write_csv(read_file(data), data)
            data = Cinematographer()
            write_csv(read_file(data), data)
            data = Country()
            write_csv(read_file(data), data)
            data = Director()
            write_csv(read_file(data), data)
            data = Genre()
            write_csv(read_file(data), data)
            data = Movie()
            write_csv(read_file(data), data)
            data = Plot()
            write_csv(read_file(data), data)
            data = Rating()
            write_csv(read_file(data), data)
            data = RunningTime()
            write_csv(read_file(data), data)
        case "1":
            actor = Actor()
            write_csv(read_file(actor), actor)
        case "2":
            actress = Actress()
            write_csv(read_file(actress), actress)
        case "3":
            cinematographer = Cinematographer()
            write_csv(read_file(cinematographer), cinematographer)
        case "4":
            country = Country()
            write_csv(read_file(country), country)
        case "5":
            director = Director()
            write_csv(read_file(director), director)
        case "6":
            genre = Genre()
            write_csv(read_file(genre), genre)
        case "7":
            movie = Movie()
            write_csv(read_file(movie), movie)
        case "8":
            plot = Plot()
            write_csv(read_file(plot), plot)
        case "9":
            rating = Rating()
            write_csv(read_file(rating), rating)
        case "10":
            running_time = RunningTime()
            write_csv(read_file(running_time), running_time)
        case _:
            print("\n" * 100)
            print("Dat is geen optie. Probeer het opnieuw\n\n")
            main()
    end_time = time.perf_counter()
    print(f"\nDone! Finished parsing in {end_time - start_time:0.04f} seconds")


# main()
# setup_database()
# setup_database("final")
convert_db()
