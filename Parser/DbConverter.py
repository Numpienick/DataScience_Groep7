from DbConnector import *
import psycopg2
from psycopg2 import sql

def convert_db():
    convert("movies")


def convert(table):
    match (table):
        case "actors":
            insert_person(get_person(table))
        case "actresses":
            insert_person(get_person(table))
        case "cinematographers":
            insert_person(get_person(table))
        case "countries":
            print()
        case "directors":
            insert_person(get_person(table))
        case "genres":
            print()
        case "movies":
            insert_showinfo(get_showinfo(table))
            # insert_show(get_show(table))
            # insert_episode(get_episode(table))
        case "plot":
            print()
        case "ratings":
            print()
            # insert_rating(get_rating(table))
        case "running-times":
            print()


def get_rating(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "SELECT distribution, amount_of_votes, rating, show_title, release_date, episode_title, season_number, episode_number FROM {}"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_rating(ratings):
    print("Inserting rating")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE "temp" (
                        "distribution" varchar,
                        "amount_of_votes" int,
                        "rating" float,
                        "show_title" varchar,
                        "release_date" varchar,
                        "episode_title" varchar,
                        "season_number" int,
                        "episode_number" int
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (distribution, amount_of_votes, rating, show_title, release_date, episode_title, season_number, episode_number) VALUES %s",
                               ratings)
                # command = """
                #               SELECT DISTINCT show.show_info_id, temp.distribution, temp.amount_of_votes, temp.rating
                #               FROM temp
                #               LEFT JOIN show
                #               ON temp.show_title = show.show_title
                #               AND temp.release_date = show.release_date
                #           """
                # cur.execute(command)
                # data = cur.fetchmany(100)
                # execute_values(cur,
                #                "INSERT INTO rating (show_info_id, distribution, amount_of_votes, rating) VALUES %s",
                #                data)
                # command = """
                #               SELECT DISTINCT episode.show_info_id, temp.distribution, temp.amount_of_votes, temp.rating
                #               FROM temp
                #               LEFT JOIN episode
                #               ON temp.show_title = episode.show_title
                #               AND temp.release_date = episode.release_date
                #               AND temp.episode_title = episode.episode_name
                #               AND temp.season_number = episode.season_number
                #               AND temp.episode_number = episode.episode_number
                #           """
                # cur.execute(command)
                # data = cur.fetchmany(100)
                # execute_values(cur,
                #                "INSERT INTO rating (show_info_id, distribution, amount_of_votes, rating) VALUES %s",
                #                data)
                command = """
                              SELECT show_info.show_info_id, temp.distribution, temp.amount_of_votes, temp.rating
                              FROM temp
                              LEFT JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date 
                          """
                cur.execute(command)
                data = cur.fetchmany(100)
                execute_values(cur,
                               "INSERT INTO rating (show_info_id, distribution, amount_of_votes, rating) VALUES %s",
                               data)
                command = "DROP TABLE temp"
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_show(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                command = "SELECT show_title, release_date, release_year, type_of_show, suspended, end_year FROM {} WHERE end_year IS NOT NULL AND release_date <> '????'"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_show(show):
    print("Inserting show")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO show (show_title, release_date, release_year, type_of_show, suspended, end_year) VALUES %s",
                               show)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_episode(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                command = "SELECT show_title, release_date, release_year, type_of_show, suspended, episode_title, season_number, episode_number FROM {} WHERE (end_year IS NULL) AND (release_date IS NOT NULL) AND ((episode_title IS NOT NULL OR season_number IS NOT NULL) OR episode_number IS NOT NULL)"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_episode(episode):
    print("Inserting episode")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        show_title varchar,
                        release_date varchar,
                        release_year varchar,
                        type_of_show varchar,
                        "suspended" bool,
                        "episode_name" varchar,
                        "season_number" int,
                        "episode_number" int
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, episode_name, season_number, episode_number) VALUES %s",
                               episode)
                command = """
                          SELECT temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended, show.show_id, temp.episode_name, temp.season_number, temp.episode_number 
                          FROM temp
                          LEFT JOIN show
                          ON temp.show_title = show.show_title
                          AND temp.release_date = show.release_date
                          """
                cur.execute(command)
                data = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO episode (show_title, release_date, release_year, type_of_show, suspended, show_id, episode_name, season_number, episode_number) VALUES %s",
                               data)
                command = "DROP TABLE temp"
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_showinfo(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                # command = "SELECT show_title, release_date, release_year, type_of_show, suspended FROM {} WHERE episode_title is NULL AND season_number is NULL AND episode_number is NULL AND end_year is NULL"
                # cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                # data = cur.fetchall()
                # return data
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                command = """
                SELECT movies.show_title, movies.release_date, movies.release_year, movies.type_of_show, movies.suspended, ratings.distribution, ratings.amount_of_votes, ratings.rating
                FROM movies 
                LEFT JOIN ratings
                ON movies.show_title = ratings.show_title
                AND movies.release_date = ratings.release_date
                WHERE movies.episode_title is NULL AND movies.season_number IS NULL AND movies.episode_number IS NULL
                """
                cur.execute(command)
                data = cur.fetchall()
                print("Data Length: " + str(len(data)))
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_showinfo(show_info):
    print("Inserting show_info")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                print("Creating temporary table")
                command = (
                    """
                    CREATE TABLE temp (
                        "temp_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
                        "show_title" varchar,
                        "release_date" varchar,
                        "release_year" varchar,
                        "type_of_show" varchar,
                        "suspended" bool,
                        "distribution" varchar,
                        "amount_of_votes" int,
                        "rating" float
                    )
                    """
                )
                #TODO: Try to link with primary key and foreign key
                cur.execute(command)
                print("Inserting data into temporary table")
                execute_values(cur,"INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, distribution, amount_of_votes, rating) VALUES %s", show_info)
                print("Altering the rating table")
                command = (
                    """
                    ALTER TABLE rating
                    ADD COLUMN "show_title" varchar
                    """
                )
                cur.execute(command)
                command = (
                    """
                    ALTER table rating
                    ADD COLUMN "release_date" varchar
                    """
                )
                cur.execute(command)
                command = (
                    """
                    ALTER table rating
                    ADD COLUMN "temp_id" int
                    """
                )
                cur.execute(command)
                command = (
                    """
                    ALTER table rating
                    ADD FOREIGN KEY ("temp_id") REFERENCES "temp" ("temp_id")
                    """
                )
                cur.execute(command)
                print("Getting the data for the rating table")
                command = "SELECT distribution, amount_of_votes, rating, show_title, release_date, temp_id  FROM temp"
                cur.execute(command)
                data = cur.fetchall()
                print("Data Length: " + str(len(data)))
                print("Inserting the data in the rating table")
                execute_values(cur, "INSERT INTO rating (distribution, amount_of_votes, rating, show_title, release_date, temp_id) VALUES %s", data)

                print("Getting data for show_info table")
                command = """
                                SELECT rating.rating_id, temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended
                                FROM temp
                                INNER JOIN rating
                                ON rating.temp_id = temp.temp_id
                                """
                cur.execute(command)
                data = cur.fetchall()
                print("Fetched the data")
                print("Data Length: " + str(len(data)))
                print("Inserting data in show_info table")
                execute_values(cur,
                               "INSERT INTO show_info (rating_id, show_title, release_date,release_year, type_of_show, suspended) VALUES %s",
                               data)
                print("Altering the rating table")
                command = (
                    """
                    ALTER TABLE rating
                    DROP COLUMN "show_title"
                    """
                )
                cur.execute(command)
                command = (
                    """
                    ALTER TABLE rating
                    DROP COLUMN "release_date"
                    """
                )
                cur.execute(command)
                command = (
                    """
                    ALTER TABLE rating
                    DROP CONSTRAINT  "rating_temp_id_fkey"
                    """
                )
                cur.execute(command)
                command = (
                    """
                    ALTER table rating
                    DROP COLUMN "temp_id"
                    """
                )
                cur.execute(command)

                print("Dropping temporary table")
                command = (
                    """
                    DROP TABLE temp
                    """
                )
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_person(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "SELECT nick_name, first_name, last_name FROM {} WHERE first_name IS NOT NULL"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_person(person):
    print("Inserting person")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, "INSERT INTO person (nick_name, last_name, first_name) VALUES %s", person)
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()
