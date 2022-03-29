import psycopg2
import os
from psycopg2 import sql
from configparser import ConfigParser
from psycopg2.extensions import AsIs
from psycopg2.sql import NULL


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
    print('Connected to database')
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
        raise err

    finally:
        if conn:
            conn.close()
        print('Connected to database')
        return conn


def convert_db(dbType="staging"):
    try:
        connFinal = connect("final")

        with connFinal.cursor() as cur:
            command = "SELECT table_name FROM information_schema.tables WHERE (table_schema = 'public') ORDER BY table_name"
            cur.execute(command)
            finalTables = cur.fetchall()

            for finalTable in finalTables:
                # new_table = table[0]
                # command = "SELECT * FROM {}".format(new_table)
                # cur.execute(command)
                # data = cur.fetchone()
                # print(data)
                command = "SELECT data_type, column_name FROM information_schema.columns WHERE TABLE_NAME = {};"
                cur.execute(sql.SQL(command).format(sql.Literal(finalTable[0])))
                finalColumns = cur.fetchall()
                # print(finalTable)
                # print(finalColumns)

                try:
                    connStaging = connect("staging")
                    with connStaging.cursor() as stagingCur:
                        command = "SELECT table_name FROM information_schema.tables WHERE (table_schema = 'public') ORDER BY table_name"
                        stagingCur.execute(command)
                        tables = stagingCur.fetchall()

                        for table in tables:
                            command = "SELECT data_type, column_name FROM information_schema.columns WHERE TABLE_NAME = {};"
                            stagingCur.execute(sql.SQL(command).format(sql.Literal(table[0])))
                            columns = stagingCur.fetchall()
                            # print(table)
                            # print(columns)
                            for finalColumn in finalColumns:
                                for column in columns:
                                    if(finalColumn == column):
                                        print("SAME")
                                        print(finalColumn)
                                        print(column)

                                        command = "SELECT {} FROM %(table)s;"
                                        stagingCur.execute(sql.SQL(command).format(sql.Identifier(column[1])), {
                                            'table': AsIs(table[0])
                                        })
                                        data = stagingCur.fetchall()
                                        i = 0
                                        for row in data:
                                            command = "INSERT INTO %(table)s ({}) VALUES (%(value)s)"
                                            if(finalColumn[0] == 'boolean' and len(finalColumn[1]) != 0):
                                                row = True
                                            if (finalColumn[0] == 'boolean' and len(finalColumn[1]) == 0):
                                                row = False

                                            cur.execute(sql.SQL(command).format(sql.Literal(AsIs(finalColumn[1]))), {
                                                'table': AsIs(finalTable[0]),
                                                'value': row[0]
                                            })
                                            if(i % 10000 == 0):
                                                print(i)
                                                print("added " + finalColumn[1] + " to " + finalTable[0])
                                                if(i == 10000):
                                                    break

                                            i = i + 1
                except Exception as err:
                    raise err
                finally:
                    if connStaging:
                        connStaging.close()


    except Exception as err:
        raise err
    finally:
        if connFinal:
            connFinal.close()

