import os
import re
import csv
import time
import os
from Parser.DbConnector import connect
from psycopg2.extras import execute_values


# Reads IMDB .list file
from playsound import playsound


def read_file(data_type):
    print(f"\nStarts reading {data_type.file}")
    startTime = time.perf_counter()
    try:
        with open("data/" + data_type.file + ".list", "r", encoding="ANSI") as f:
            txt = f.read()
        txt = re.sub(';', ':', txt)
        txt = re.sub('\\\\', ' ', txt)

        # Some files needs a cleanup step before the regex, this if statement will trigger
        if len(data_type.clean_file_regex.strip()) > 0:
            print(f"\nStarts cleaning {data_type.file}")
            cleaned = re.search(data_type.clean_file_regex, str(txt))
            txt = str(cleaned.group("data"))
            end_time_clean = time.perf_counter()
            print(f"\033[1;32mDone cleaning {data_type.file} in {end_time_clean - startTime:0.04f} seconds\033[1;37m")
            print(f"\nContinuing reading {data_type.file}")

        data = re.findall(data_type.regex, str(txt))
        end_time = time.perf_counter()
        print(f"\033[1;32mDone reading {data_type.file} in {end_time - startTime:0.04f} seconds\033[1;37m")
        return data
    except Exception as e:
        #playsound(os.path.abspath('./assets/fail.wav'))
        print(e)


# Writes csv from read file
def write_csv(data, data_type):
    start_time = time.perf_counter()
    name = data_type.file
    print(f"\nStarts writing {name}")
    pattern = re.compile(data_type.regex)
    groups = str(pattern.groupindex)
    headers = re.findall(r"([_a-z]+)", groups, re.M | re.I)

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
            if name == "actors" or name == "actresses" or name == "cinematographers" or name == "directors" or "credit_only" in headers or "uncredited" in headers or "suspended" in headers or "music_video" in headers or "scenes_deleted" in headers or "rumored" in headers or "approximated" in headers or "archive_footage" in headers:
                for line in data:
                    listed = list(line)
                    if name == "actors" or name == "actresses" or name == "cinematographers" or name == "directors":
                        # Fills the empty names with the last filled one
                        if name == "actors":
                            listed.insert(22, False)
                        if name == "actresses":
                            listed.insert(22, True)
                        if line[0] == '' and line[1] == '' and line[2] == '':
                            listed[0] = old_nickname
                            listed[1] = old_lastname
                            listed[2] = old_firstname
                        else:
                            old_nickname = line[0]
                            old_lastname = line[1]
                            old_firstname = line[2]
                    if "credit_only" in headers or "uncredited" in headers or "suspended" in headers or "music_video" in headers or "scenes_deleted" in headers or "rumored" in headers or "approximated" in headers or "archive_footage" in headers:
                        # Loops through every column that is a boolean and puts true if it's not empty
                        if "credit_only" in headers:
                            credit_only = headers.index("credit_only")
                            listed[credit_only] = len(line[credit_only]) > 0  # Fill the field of the column in the current line with a bool if the column field is empty or not
                        if "uncredited" in headers:
                            uncredited = headers.index("uncredited")
                            listed[uncredited] = len(line[uncredited]) > 0
                        if "suspended" in headers:
                            suspended = headers.index("suspended")
                            listed[suspended] = len(line[suspended]) > 0
                        if "music_video" in headers:
                            music_video = headers.index("music_video")
                            listed[music_video] = len(line[music_video]) > 0
                        if "scenes_deleted" in headers:
                            scenes_deleted = headers.index("scenes_deleted")
                            listed[scenes_deleted] = len(line[scenes_deleted]) > 0
                        if "rumored" in headers:
                            rumored = headers.index("rumored")
                            listed[rumored] = len(line[rumored]) > 0
                        if "approximated" in headers:
                            approximated = headers.index("approximated")
                            listed[approximated] = len(line[approximated]) > 0
                        if "including_commercials" in headers:
                            including_commercials = headers.index("including_commercials")
                            listed[including_commercials] = len(line[including_commercials]) > 0
                        if "archive_footage" in headers:
                            archive_footage = headers.index("archive_footage")
                            listed[archive_footage] = len(line[archive_footage]) > 0
                    tuple_line = tuple(listed)
                    writer.writerow(tuple_line)
            else:
                writer.writerows(data)

            end_time = time.perf_counter()
            print(f"\033[1;32mDone writing to {name}.csv in {end_time - start_time:0.04f} seconds\033[1;37m")
    except Exception as e:
        print(f"\033[1;31mSomething went wrong trying to write to {data_type.file}!\033[1;37m")
        #playsound(os.path.abspath('./assets/fail.wav'))
        print(e)


def write_csv_from_table(view):
    try:
        filename = view
        filepath = "NewData/" + filename + '.csv'
        if os.path.exists(filepath):
            os.remove(filepath)
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                if view == 'movie_rating_actrice_count':
                    command = """
                    CREATE TABLE "temp" (
                        "show_title" varchar,
                        "rating" float,
                        "total_roles" int
                    ) 
                    """
                if view == 'plot_rating':
                    command = """
                    CREATE TABLE "temp" (
                        "plot" varchar,
                        "rating" float
                    ) 
                    """
                if view == 'running_times_rating':
                    command = """
                    CREATE TABLE "temp" (
                        "running_times" int,
                        "rating" float
                    ) 
                    """
                cur.execute(command)
                command = "SELECT * FROM {}".format(view)
                cur.execute(command)
                data = cur.fetchall()
                execute_values(cur, "INSERT INTO temp VALUES %s", data)
                with open(filepath, 'x', encoding="utf-8", newline='') as f:
                    cur.copy_to(f, 'temp', sep=';')

                    f.close()
                command = "DROP TABLE temp"
                cur.execute(command)
    except Exception as err:
        # playsound(os.path.abspath('./assets/fail.wav'))
        raise err
    finally:
        if conn:
            conn.close()

