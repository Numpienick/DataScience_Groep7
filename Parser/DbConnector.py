import psycopg2
import os
from psycopg2 import sql
from configparser import ConfigParser
from psycopg2.extensions import AsIs
from psycopg2.sql import NULL
from psycopg2.extras import execute_values
from datetime import datetime


def config(section='staging'):
    """
    Returns an object containing the properties and values needed to connect to the corresponding database

    :param section: Is either "staging" or "final". Defines the section of the config file in database.ini.
    If not defined defaults to "staging"
    """
    while section not in ["staging", "final"]:
        print(f'Wrong dbType: {section}\nIt should be either "staging" or "final"')
        return

    parser = ConfigParser()
    parser.read('database.ini')

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found in database.ini".format(section))
    return db


def connect(dbType='staging'):
    """
    Connects to the database corresponding to dbType

    :param dbType: Is either "staging" or "final". Defines the database that will be connected to.
    If not defined defaults to "staging"
    """
    while dbType not in ["staging", "final"]:
        print(f'Wrong dbType: {dbType}\nIt should be either "staging" or "final"')
        return

    try:
        params = config(dbType)
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Fill the Database

        # filename = "actors"
        # filepath = 'output/' + filename + '.csv'
        # print(filepath)
        # with open(filepath, 'r', encoding="ANSI", newline='') as f:
        #     next(f)
        #     cur.copy_from(f, filename, sep=';', null="")
        # conn.commit()

        # fill_db(conn)

        # Empty The Database
        # cur.execute("DELETE FROM actors")
        # conn.commit()
        # empty_db(conn, dbType, "actors")

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    print('Connected to ' + dbType + ' database')
    return conn


def setupDatabase(dbType='staging'):
    """
    Drops and recreates the database with tables provided by the corresponding setup script

    :param dbType: Is either "staging" or "final". Defines the database that needs to be set up.
    If not defined defaults to "staging"
    """
    while dbType not in ["staging", "final"]:
        print(f'Wrong dbType: {dbType}\nIt should be either "staging" or "final"')
        return

    params = config(dbType)
    dbName = params['database']
    owner = params['user']
    params["database"] = ""
    try:  # Recreates the database
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        with conn.cursor() as cur:
            dropCommand = "DROP DATABASE IF EXISTS {} WITH (FORCE);"
            cur.execute(sql.SQL(dropCommand).format(sql.Identifier(dbName)))
            print(f"Database {dbName} has been successfully dropped")

            createCommand = "CREATE DATABASE {} OWNER %(owner)s;"
            cur.execute(sql.SQL(createCommand).format(sql.Identifier(dbName)), {
                'owner': owner
            })
            print(f"Database {dbName} has been successfully created and is owned by {owner}")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()

    if dbType == "staging":
        filename = "Staging_DataScience_Groep7.sql"
    elif dbType == "final":
        filename = "DataScience_Groep7.sql"

    with open(f"../SQL/{filename}", "r") as f:
        try:  # Reads the setup script
            sqlFile = f.read()
            sqlCommands = sqlFile.split(';')
        except Exception as err:
            raise (err)

    try:  # Execute all the commands in setup script
        with connect(dbType) as connection:
            with connection.cursor() as cur:
                for command in sqlCommands:
                    if not command.isspace():
                        try:
                            cur.execute(command)
                        except Exception as err:
                            print(
                                f"Something went wrong: {err}\nThis happened with the following command: {command}\nClosing the transaction...")
                            cur.close()
                            break
                if not cur.closed:
                    print("Finished creating all the tables")
    except Exception as err:
        raise err

    finally:
        if connection:
            connection.close()

    fill_db()


def fill_db(dbType='staging'):
    """
        Fills the staging database with data.

        :param dbType: Is either "staging" or "final". Defines the database that needs to be set up.
        If not defined defaults to "staging"
        """
    while dbType not in ["staging", "final"]:
        print(f'Wrong dbType: {dbType}\nIt should be either "staging" or "final"')
        return

    try:  # Retrieves the data from files and puts it in the correct table.
        params = config(dbType)
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        if (dbType == 'staging'):
            path = 'output'
            files = os.listdir(path)

            for file in files:
                if file.endswith(".csv"):
                    with conn.cursor() as cur:
                        filename = file.split(sep='.')[0]
                        filepath = 'output/' + filename + '.csv'
                        if filename == "running-times":
                            filename = "running_times"
                        print(f"Started transferring {filename} data to database ")
                        with open(filepath, 'r', encoding="ANSI", newline="") as f:
                            next(f)
                            copy_sql = """
                                            COPY {}
                                            FROM stdin
                                            CSV DELIMITER as ';'
                                            """.format(filename)
                            cur.copy_expert(sql=copy_sql, file=f)
                        print(f"Finished transferring {filename} data to database ")

    except Exception as err:
        print(err)
        raise err

    finally:
        if conn:
            conn.close()
        print('Connected to database')
        return conn


def convert_db(dbType="staging"):
    # fill_shows("show", get_shows())
    # InsertRole(GetActors())
    # insert_genres(get_genres())
    # insert_countries(get_countries())
    insert_known_as(get_known_as("actors"))
    # insert_person(get_persons("actors"), "actors")
    # insert_plot(get_plot())
    # insert_ratings(get_ratings())
    # InsertCinematographers(GetCinematographers())
    # InsertPerson(GetPerson("actresses"))
    # InsertPerson(GetPerson("cinematographers"))
    # InsertPerson(GetPerson("directors"))
    # InsertRole(GetRole("actors"))
    # InsertPlot(GetPlot("plot"))
    # InsertRatings(GetRatings("ratings"))


def get_shows():
    print("Getting shows")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM movies")
                data = cur.fetchmany(100)
                print(data[0][9])
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def fill_shows(table, show):
    print("Inserting shows")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                for tuple in show:
                    print(tuple)
                    if tuple[9] == '????':
                        date = NULL

                    insertCommand = "INSERT INTO {} (end_year) VALUES (%(data)s);"
                    cur.execute(sql.SQL(insertCommand).format(sql.Identifier(table)), {
                        'data': date
                    })
                    # execute_values(cur, "INSERT INTO show (end_year) VALUES %s", show)
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_persons(table):
    print("Getting " + table + " from staging")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                if table == "actors":
                    cur.execute("SELECT * from role_actors")
                    data = cur.fetchmany(100)
                    return data
                if table == "actresses":
                    cur.execute("SELECT * from role_actresses")
                    data = cur.fetchmany(100)
                    return data
                if table == "cinematographers":
                    cur.execute("SELECT * from get_cinematographers")
                    data = cur.fetchmany(100)
                    return data
                if table == "directors":
                    cur.execute("SELECT * from get_directors")
                    data = cur.fetchmany(100)
                    return data
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
                    data = cur.fetchmany(100)
                    return data
                if table == "actresses":
                    cur.execute("SELECT * from get_known_as_actresses")
                    data = cur.fetchmany(100)
                    return data
                if table == "cinematographers":
                    cur.execute("SELECT * from get_known_as_cinematographers")
                    data = cur.fetchmany(100)
                    return data
                if table == "directors":
                    cur.execute("SELECT * from get_known_as_directors")
                    data = cur.fetchmany(100)
                    return data
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_plot():
    print("Getting plot")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT plot, written_by FROM plot")
                data = cur.fetchmany(100)
                return data
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_ratings():
    print("Getting ratings")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT distribution, amount_of_votes, rating FROM ratings")
                data = cur.fetchmany(100)
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_countries():
    print("Getting countries")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT countries_of_origin FROM countries")
                data = cur.fetchmany(100)
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_genres():
    print("Getting genres")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT genre FROM genres")
                data = cur.fetchmany(100)
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_ratings(ratings):
    print("Inserting ratings")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, "INSERT INTO rating (distribution, amount_of_votes, rating) VALUES %s", ratings)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_plot(plot):
    print("Inserting plot")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, "INSERT INTO plot (plot, written_by) VALUES %s", plot)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()

    """
    Inserts person (actor, actress, director or cinematographer) to final db from staging db

    :param person: is the list of tuples to be inserted
    :param type: is the type of person, can be either: actors, actresses, cinematographers or directors
    """


def insert_person(person, type):
    print("Inserting role")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                # TODO: show_info_id
                if type == "actors" or type == "actresses":
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, character_name, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored, motion_capture, role_position) VALUES %s",
                                   person)
                if type == "cinematographers":
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, type_of_cinematographer, segment, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                                   person)
                if type == "directors":
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, type_of_director, character_name, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                                   person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_known_as(knownAs):
    print("Inserting known_as")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO also_known_as (also_known_as) VALUES %s RETURNING also_known_as_id;",
                               knownAs)
                test = cur.fetchall()
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_countries(countries):
    print("Inserting countries")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO country (country_name) VALUES %s",
                               countries)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_genres(genres):
    print("Inserting genres")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO genre (genre_name) VALUES %s",
                               genres)
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()
