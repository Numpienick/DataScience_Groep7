import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from configparser import ConfigParser
from psycopg2.extensions import AsIs
from psycopg2.sql import NULL
from psycopg2.extras import execute_values



def config(section='staging'):
    """
    Returns an object containing the properties and values needed to connect to the corresponding database

    :param section: Is either "staging" or "final". Defines the section of the config file in database.ini.
    If not defined defaults to "staging"
    """
    while section not in ["staging", "final"]:
        print(f'\033[1;31mWrong dbType: {section}\nIt should be either "staging" or "final"\033[1;37m')
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
        print(f'\033[1;31mWrong dbType: {db_type}\nIt should be either "staging" or "final"\033[1;37m')
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
        print(f'\033[1;31mWrong dbType: {db_type}\nIt should be either "staging" or "final"\033[1;37m')
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
            print(f"\033[1;32m\nDatabase {db_name} has been successfully dropped\033[1;37m")

        with conn.cursor() as cur:
            create_command = "CREATE DATABASE {} OWNER %(owner)s;"
            cur.execute(sql.SQL(create_command).format(sql.Identifier(db_name)), {
                'owner': owner
            })
            print(f"\033[1;32m\nDatabase {db_name} has been successfully created and is owned by {owner}\033[1;37m")
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
                                f"\033[1;31mSomething went wrong: {err}\nThis happened with the following command: {command}\nClosing the transaction...\033[1;37m")
                            cur.close()
                            break
                if not cur.closed:
                    print("\033[1;32mFinished creating all the tables\033[1;37m")
    except Exception as err:
        raise err

    finally:
        if conn:
            conn.close()
