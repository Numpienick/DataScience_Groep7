from DbConnector import *
from Parser.classes.Plot import Plot
import psycopg2
from psycopg2 import sql


def convert_db():
    add_indices()


def convert(table):
    table.insert_table(table.get_table())


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
                execute_values(cur,
                               "INSERT INTO also_known_as (also_known_as) VALUES %s RETURNING also_known_as_id;",
                               known_as)
                test = cur.fetchall()
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()
