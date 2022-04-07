import os
import time

from playsound import playsound

from Parser.CSVWriter import write_csv, read_file, write_csv_from_table
from Parser.DbConnector import setup_database
from Parser.DbConverter import convert_db, convert, add_indices, convert_to_loggable

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

# Calls the correct csv files with a choice menu
def csv_caller():
    print("Welke dataset wilt u omzetten naar een CSV bestand?")
    print("1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movie \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal")

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
    # playsound(os.path.abspath('./assets/success.wav'))


def db_converter_caller():
    print("We gaan aan de slag met het omzetten van de staging database naar de final database!\n")
    print("Welke tabel wilt u omzetten naar de Final database?")
    print("Note: Zorg ervoor dat de films eerst bestaan en dat de rest dan wordt uitgevoerd, indien je de volgorde niet weet kunt u voor 0 kiezen. Dit werkt altijd.")
    print("1. Actors\n2. Actresses \n3. Cinematographers \n4. Countries \n5. Directors \n6. Genres \n7. Movies \n8. Plot \n9. Ratings \n10. Running Times \n0. Allemaal")

    data_set_choice = input()
    start_time = time.perf_counter()

    match data_set_choice:
        case "0":
            convert(Movie())
            convert(Actor())
            convert(Actress())
            convert(Cinematographer())
            convert(Country())
            convert(Director())
            convert(Genre())
            convert(Plot())
            convert(Rating())
            convert(RunningTime())
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
            print("Dat is geen optie. Probeer het opnieuw\n\n")
            main()
    end_time = time.perf_counter()
    print(f"\nDone! Finished converting in {end_time - start_time:0.04f} seconds")
    # playsound(os.path.abspath('./assets/success.wav'))


# Main function, provides info and choice
def main():
    print("Welkom bij de IMDB Data-Parser van groep 7")
    print("Wat wilt u doen?")
    print("1. Dataset omzetten naar CSV?\n2. Database opzetten?\n3. Staging database omzetten naar Final database?\n4. De afsluiting, indices creeëren, tables omzetten naar LOGGABLE etc.\n5. Allemaal, in goede volgorde\n6. Haal data voor r-modellen op")
    menu_choice = input()
    match menu_choice:
        case "1":  # CSV_Caller
            csv_caller()
        case "2":  # Setup DB
            print("Welke database wilt u opzetten?")
            print("1. Staging database\n2. Final database\n3. Allebei")
            db_choice = input()
            match db_choice:  # DB Choice
                case "1":
                    setup_database()
                case "2":
                    setup_database("final")
                case "3":
                    setup_database()
                    setup_database("final")
        case "3":  # DB Converter
            db_converter_caller()
        case "4":  # Finalize
            convert_to_loggable()
            add_indices()
        case "5":  # All
            csv_caller()
            setup_database()
            setup_database("final")
            db_converter_caller()
            convert_to_loggable()
            add_indices()
        case "6":
            write_csv_from_table("movie_rating_actrice_count")
            write_csv_from_table("plot_rating")


# Calls the main function (at the bottom to ensure all functions are available)
main()
