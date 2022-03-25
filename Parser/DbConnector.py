import psycopg2
import os
from configparser import ConfigParser


def config(section = 'postgresql'):
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


def connect():
    try:
        params = config()

        print('Connecting to the database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        #Fill the Database
        # fill_db(conn)

        #Empty The Database
        #empty_db(conn)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    print('Connected to database')
    conn.close()
    return conn


def fill_db(conn):
    cur = conn.cursor()
    filenames = ['actor', 'actresses', 'cinematographers', 'countries', 'directors', 'genres', 'movies', 'plot',
                 'ratings', 'running-times']
    for filename in filenames:
        filepath = 'output/' + filename + '.csv'
        print(filepath)
        filesize = os.stat(filepath).st_size
        if filename == 'running-times':
            with open(filepath, 'r', encoding="ANSI", newline='') as f:
                next(f)
                cur.copy_from(f, 'running_time', sep=';', null="")
            conn.commit()
        else:
            with open(filepath, 'r', encoding="ANSI", newline='') as f:
                next(f)
                cur.copy_from(f, 'running_time', sep=';', null="")
            conn.commit()


def empty_db(conn):
    cur = conn.cursor()
    tablenames = ['actor', 'actresses', 'cinematographers', 'countries', 'directors', 'genres', 'movies', 'plot',
                 'ratings', 'running_time']
    for tablename in tablenames:
        cur.execute("DELETE FROM {table_name }")
        conn.commit()

def main():
    config()
    connect()


main()




