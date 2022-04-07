import psycopg2
import os

from playsound import playsound
from psycopg2 import sql
from psycopg2.extensions import AsIs
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


def connect(db_type='staging'):
    """
    Connects to the database corresponding to dbType.
    Autocommit is turned on.

    :param db_type: Is either "staging" or "final". Defines the database that will be connected to.
    If not defined defaults to "staging"
    """
    while db_type not in ["staging", "final"]:
        print(f'Wrong dbType: {db_type}\nIt should be either "staging" or "final"')
        return

    try:
        params = config(db_type)
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    print('Connected to ' + db_type + ' database')
    return conn


def setup_database(db_type='staging'):
    """
    Drops and recreates the database with tables provided by the corresponding setup script

    :param db_type: Is either "staging" or "final". Defines the database that needs to be set up.
    If not defined defaults to "staging"
    """
    while db_type not in ["staging", "final"]:
        print(f'Wrong dbType: {db_type}\nIt should be either "staging" or "final"')
        return

    params = config(db_type)
    db_name = params['database']
    owner = params['user']
    params["database"] = ""
    try:  # Recreates the database
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        with conn.cursor() as cur:
            drop_command = "DROP DATABASE IF EXISTS {} WITH (FORCE);"
            cur.execute(sql.SQL(drop_command).format(sql.Identifier(db_name)))
            print(f"Database {db_name} has been successfully dropped")

        with conn.cursor() as cur:
            create_command = "CREATE DATABASE {} OWNER %(owner)s;"
            cur.execute(sql.SQL(create_command).format(sql.Identifier(db_name)), {
                'owner': owner
            })
            print(f"Database {db_name} has been successfully created and is owned by {owner}")
            playsound(os.path.abspath("./assets/success.wav"))
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()

    filename = "DataScience_Groep7.sql" if db_type == "final" else "Staging_DataScience_Groep7.sql"
    with open(f"../SQL/{filename}", "r") as f:
        try:  # Reads the setup script
            sql_file = f.read()
            sql_commands = sql_file.split(';')
        except Exception as err:
            raise err

    try:  # Execute all the commands in setup script
        with connect(db_type) as connection:
            with connection.cursor() as cur:
                for command in sql_commands:
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
        if conn:
            conn.close()

    if db_type == "staging":
        fill_staging_db()


def fill_staging_db():
    """
        Fills the staging database with data.
    """

    try:  # Retrieves the data from files and puts it in the correct table.
        params = config("staging")
        conn = psycopg2.connect(**params)
        conn.autocommit = True
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
                    playsound(os.path.abspath("./assets/success.wav"))

    except Exception as err:
        print(f"Something went wrong trying to copy {filename} to the database!")
        raise err

    finally:
        if conn:
            conn.close()


