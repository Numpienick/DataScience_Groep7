import psycopg2
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
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    return conn
