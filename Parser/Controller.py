import os
import time
import multiprocessing as mp
from multiprocessing import Process

from Parser.CSVWriter import write_csv, read_file, write_csv_from_table
from Parser.DbConnector import setup_database
from Parser.DbConverter import convert_db, convert, add_indices, convert_to_loggable, fill_staging_db

from Parser.classes.Actor import Actor
from Parser.classes.Actress import Actress
from Parser.classes.Cinematographer import Cinematographer
from Parser.classes.Country import Country
from Parser.classes.Director import Director
from Parser.classes.Genre import Genre
from Parser.classes.Movie import Movie
from Parser.classes.Plot import Plot
from Parser.classes.Rating import Rating
from Parser.classes.RunningTime import RunningTime


data_sets = [
    Actor(),
    Actress(),
    Cinematographer(),
    Country(),
    Director(),
    Genre(),
    Movie(),
    Plot(),
    Rating(),
    RunningTime(),
]


def convert_to_csv(data_type):
    """
    Calls the CSVWriter functions to convert the given Dataset to CSV
    :param  data_type: A Dataset that will be converted to CSV
    """
    write_csv(read_file(data_type), data_type)


def ask_for_dataset():
    print("\033[1;34mWelke dataset wilt u omzetten naar een CSV bestand?")
    print(
        "\033[1;34m1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movie \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal\033[1;37m")

    try:
        data_set_choice = int(input())
    except ValueError:
        print("\n" * 100)
        print("\033[1;31mDat is geen optie. Probeer het opnieuw\n\n\033[1;37m")
        ask_for_dataset()

    if data_set_choice not in range(0, 11):
        print("\n" * 100)
        print("\033[1;31mDat is geen optie. Probeer het opnieuw\n\n\033[1;37m")
        ask_for_dataset()
    return data_set_choice


# Calls the correct csv files with a choice menu
def csv_caller(data_set_choice):
    start_time = time.perf_counter()

    match data_set_choice:
        case 0:
            pool = mp.Pool(mp.cpu_count())
            pool.map(convert_to_csv, [*data_sets])
            pool.close()
            pool.join()
        case 1:
            actor = Actor()
            write_csv(read_file(actor), actor)
        case 2:
            actress = Actress()
            write_csv(read_file(actress), actress)
        case 3:
            cinematographer = Cinematographer()
            write_csv(read_file(cinematographer), cinematographer)
        case 4:
            country = Country()
            write_csv(read_file(country), country)
        case 5:
            director = Director()
            write_csv(read_file(director), director)
        case 6:
            genre = Genre()
            write_csv(read_file(genre), genre)
        case 7:
            movie = Movie()
            write_csv(read_file(movie), movie)
        case 8:
            plot = Plot()
            write_csv(read_file(plot), plot)
        case 9:
            rating = Rating()
            write_csv(read_file(rating), rating)
        case 10:
            running_time = RunningTime()
            write_csv(read_file(running_time), running_time)
    end_time = time.perf_counter()
    print(f"\033[1;32m\nDone! Finished parsing in {end_time - start_time:0.04f} seconds\033[1;37m")
    # playsound(os.path.abspath('./assets/success.wav'))


def db_converter_caller():
    print("\033[1;34mWe gaan aan de slag met het omzetten van de staging database naar de final database!\n")
    print("\033[1;34mWelke tabel wilt u omzetten naar de Final database?")
    print(
        "\033[1;33mNote: Zorg ervoor dat de films eerst bestaan en dat de rest dan wordt uitgevoerd, indien je de volgorde niet weet kunt u voor 0 kiezen. Dit werkt altijd.")
    print(
        "\033[1;34m1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movies \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal\033[1;37m")

    data_set_choice = input()
    start_time = time.perf_counter()

    match data_set_choice:
        case "0":
            for dataset in data_sets:
                if dataset.file == "movies":
                    convert(dataset)
                    data_sets.remove(dataset)
            pool = mp.Pool(mp.cpu_count())
            pool.map(convert, [*data_sets])
            pool.close()
            pool.join()
        case "1":
            convert(Actor())
        case "2":
            convert(Actress())
        case "3":
            convert(Cinematographer())
        case "4":
            convert(Country())
        case "5":
            convert(Director())
        case "6":
            convert(Genre())
        case "7":
            convert(Movie())
        case "8":
            convert(Plot())
        case "9":
            convert(Rating())
        case "10":
            convert(RunningTime())
        case _:
            print("\n" * 100)
            print("\033[1;31mDat is geen optie. Probeer het opnieuw\n\n\033[1;37m")
            main()
    end_time = time.perf_counter()
    print(f"\033[1;32m\nDone! Finished converting in {end_time - start_time:0.04f} seconds\033[1;37m")
    # playsound(os.path.abspath('./assets/success.wav'))


# Main function, provides info and choice
def main():
    print("\033[1;31m _____ __  __ _____  ____    _____        __        _____        _")
    print("\033[1;31m|_   _|  \/  |  __ \|  _ \  |_   _|      / _|      |  __ \      | |                                     ")
    print("\033[1;37m  | | | \  / | |  | | |_) |   | |  _ __ | |_ ___   | |  | | __ _| |_ __ _ _ __ ___   _____   _____ _ __ ")
    print("\033[1;37m  | | | |\/| | |  | |  _ <    | | | '_ \|  _/ _ \  | |  | |/ _` | __/ _` | '_ ` _ \ / _ \ \ / / _ \ '__|")
    print("\033[1;34m _| |_| |  | | |__| | |_) |  _| |_| | | | || (_) | | |__| | (_| | || (_| | | | | | | (_) \ V /  __/ |   ")
    print("\033[1;34m|_____|_|  |_|_____/|____/  |_____|_| |_|_| \___/  |_____/ \__,_|\__\__,_|_| |_| |_|\___/ \_/ \___|_|   ")

    print("\033[1;34m Welkom bij de IMDB Datamover van groep 7")
    print("\033[1;34mWat wilt u doen?")
    print(
        "\033[1;34m1. Dataset omzetten naar CSV?\n2. Database opzetten?\n3. Staging database omzetten naar Final database?\n4. De afsluiting, indices creeëren, tables omzetten naar LOGGABLE etc.\n5. Allemaal, in goede volgorde\n6. Haal data voor r-modellen op\033[1;37m")
    menu_choice = input()
    match menu_choice:
        case "1":  # CSV_Caller
            csv_caller(ask_for_dataset())
        case "2":  # Setup DB
            print("\033[1;34mWelke database wilt u opzetten?")
            print("\033[1;34m1. Staging database\n2. Final database\n3. Allebei\033[1;37m")
            db_choice = input()
            match db_choice:  # DB Choice
                case "1":
                    setup_database()
                case "2":
                    setup_database("final")
                case "3":
                    processes = [
                        Process(target=setup_database, args=()),
                        Process(target=setup_database, args=(["final"]))]
                    for p in processes:
                        p.start()
                    for p in processes:
                        p.join()
                    fill_staging_db()
        case "3":  # DB Converter
            db_converter_caller()
        case "4":  # Finalize
            convert_to_loggable()
            add_indices()
        case "5":  # All
            choice = ask_for_dataset()

            processes = [
                Process(target=setup_database, args=()),
                Process(target=setup_database, args=(["final"])),
                Process(target=csv_caller, args=([choice]))
            ]
            for p in processes:
                p.start()

            for p in processes:
                p.join()

            fill_staging_db()
            db_converter_caller()
            convert_to_loggable()
            add_indices()
        case "6":
            write_csv_from_table("movie_rating_actrice_count")
            write_csv_from_table("plot_rating")
            write_csv_from_table("running_times_rating")
    #playsound(os.path.abspath("assets/success.wav"))

# Calls the main function (at the bottom to ensure all functions are available)
if __name__ == "__main__":
    main()
