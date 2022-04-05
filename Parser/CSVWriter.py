import re
import csv
import time


# Reads IMDB .list file
def read_file(data_type):
    print(f"\nStarts reading {data_type.file}")
    startTime = time.perf_counter()
    try:
        with open("data/" + data_type.file + ".list", "r", encoding="ANSI") as f:
            data = data_type.section_data(f)
            if data != "":
                data = re.findall(data_type.regex, data)
                return data
            txt = f.read()
            txt = re.sub(';', ':', txt)
            txt = re.sub('\\\\', ' ', txt)

            # Some files needs a cleanup step before the regex, this if statement will trigger
            if len(data_type.clean_file_regex.strip()) > 0:
                print(f"\nStarts cleaning {data_type.file}")
                cleaned = re.search(data_type.clean_file_regex, str(txt))
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
