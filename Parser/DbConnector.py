import psycopg2
import os
from psycopg2 import sql
from configparser import ConfigParser


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


def connect(dbType = 'staging'):
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

        #Fill the Database

        # filename = "actors"
        # filepath = 'output/' + filename + '.csv'
        # print(filepath)
        # with open(filepath, 'r', encoding="ANSI", newline='') as f:
        #     next(f)
        #     cur.copy_from(f, filename, sep=';', null="")
        # conn.commit()

        #fill_db(conn)

        #Empty The Database
        cur.execute("DELETE FROM actors")
        conn.commit()
        # empty_db(conn, dbType, "actors")

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    print('Connected to database')
    return conn


def setupDatabase(dbType = 'staging'):
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
    try:    # Recreates the database
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
        try:    # Reads the setup script
            sqlFile = f.read()
            sqlCommands = sqlFile.split(';')
        except Exception as err:
            raise(err)

    try:    # Execute all the commands in setup script
        with connect(dbType) as connection:
            with connection.cursor() as cur:
                for command in sqlCommands:
                    if not command.isspace():
                        try:
                            cur.execute(command)
                        except Exception as err:
                            print(f"Something went wrong: {err}\nThis happened with the following command: {command}\nClosing the transaction...")
                            cur.close()
                            break
                if not cur.closed:
                    print("Finished creating all the tables")
    except Exception as err:
        raise err

    finally:
        if connection:
            connection.close()


def fill_db(conn):
    cur = conn.cursor()
    filenames = ['actors', 'actresses', 'cinematographers', 'countries', 'directors', 'genres', 'movies', 'plot',
                 'ratings', 'running-times']
    for filename in filenames:
        filepath = 'output/' + filename + '.csv'
        print(filepath)
        if filename == 'running-times':
            with open(filepath, 'r', encoding="ANSI", newline='') as f:
                next(f)
                cur.copy_from(f, 'running_time', sep=';', null="")
            conn.commit()
        else:
            with open(filepath, 'r', encoding="ANSI", newline='') as f:
                next(f)
                cur.copy_from(f, filename, sep=';', null="")
            conn.commit()


def empty_db(conn, dbType, table_name):
    cur = conn.cursor()
    params = config(dbType)
    dbName = params['database']
    createCommand = "DELETE FROM %(table_name)s;"
    cur.execute(sql.SQL(createCommand).format(sql.Identifier(dbName)), {
            'table_name': table_name
        })
    conn.commit()

def main():
    config()
    connect()


main()




