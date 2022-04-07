import os
import multiprocessing as mp
import time

from DbConnector import *
from Parser.classes.Plot import Plot
import psycopg2
from psycopg2 import sql


def convert_db():
    add_indices()


def convert(table):
    table.insert_table(table.get_table())


def copy_csv_to_staging(filename):
    """
    Copies the given csv file to the staging database
    :param filename: The name of the csv file
    """
    print(f"\nStarted transferring {filename} data to database")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                with open('output/' + filename + '.csv', 'r', encoding="ANSI", newline="") as f:
                    if filename == "running-times":
                        filename = "running_times"
                    next(f)
                    copy_sql = """
                              COPY {}
                              FROM stdin
                              CSV DELIMITER as ';'
                                          """.format(filename)
                    cur.copy_expert(sql=copy_sql, file=f)
    except Exception as err:
        print(f"\033[1;31m\nSomething went wrong trying to transfer {filename} to the staging database\033[1;37m")
        raise err
    finally:
        if conn:
            conn.close()
    print(f"\nFinished transferring {filename} to the staging database\033[1;37m")


def fill_staging_db():
    """
    Copies all the .csv files located in /output to the staging database
    """
    print("\nStarting filling of the staging database!")
    start_time = time.perf_counter()
    try:  # Retrieves the data from files and puts it in the correct table.
        path = 'output'
        files = os.listdir(path)
        filenames = []
        for file in files:
            if file.endswith(".csv"):
                filename = file.split(sep='.')[0]
                filenames.append(filename)
        pool = mp.Pool(mp.cpu_count())
        pool.map(copy_csv_to_staging, [*filenames])
        pool.close()
        pool.join()

    except Exception as err:
        print(f"\n\033[1;31mSomething went wrong trying to transfer {filename} to the staging database\033[1;37m")
        raise err
    end_time = time.perf_counter()
    print(f"\033[1;32m\nDone!! Finished filling the staging database in {end_time - start_time:0.04f} seconds\033[1;37m")


def add_indices():
    print("Creating indices")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = "CREATE INDEX idx_rating ON rating(rating);"
                cur.execute(command)
                command = "CREATE INDEX idx_person_last_name ON person(last_name);"
                cur.execute(command)
                command = "CREATE INDEX idx_show_info_show_title ON show_info(show_title);"
                cur.execute(command)
                print("Finished creating indices")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def convert_to_loggable():
    print("Converting to loggable")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT table_name AS full_rel_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cur.fetchall()
                for table in tables:
                    cur.execute("ALTER TABLE %s SET LOGGED", table)
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_known_as(table):
    print("Getting " + table + " from staging")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                if table == "actors":
                    cur.execute("SELECT * from get_known_as_actors")
                    data = cur.fetchall()
                    return data
                if table == "actresses":
                    cur.execute("SELECT * from get_known_as_actresses")
                    data = cur.fetchall()
                    return data
                if table == "cinematographers":
                    cur.execute("SELECT * from get_known_as_cinematographers")
                    data = cur.fetchall()
                    return data
                if table == "directors":
                    cur.execute("SELECT * from get_known_as_directors")
                    data = cur.fetchall()
                    return data
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_known_as(known_as):
    print("Inserting known_as")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, "INSERT INTO also_known_as (also_known_as) VALUES %s RETURNING also_known_as_id;", known_as)
                test = cur.fetchall()
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()
