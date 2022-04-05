from DbConnector import *
import psycopg2
from psycopg2 import sql


def convert_db():
    convert("movies")


def convert(table):
    match (table):
        case "actors":
            print()
        case "actresses":
            print()
        case "cinematographers":
            print()
        case "countries":
            print()
        case "directors":
            print()
        case "genres":
            print()
        case "movies":
            insert_showinfo(get_showinfo(table))
            insert_show(get_show(table))
            insert_episode(get_episode(table))
        case "plot":
            print()
        case "ratings":
            print()
        case "running-times":
            print()


def get_show(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                print("Getting all data needed for the show table from staging database")
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                # Selects the data of all the shows in the movies.csv file.
                command = "SELECT * FROM movies WHERE end_year IS NOT NULL AND release_date <> '????'"
                cur.execute(command)
                data = cur.fetchall()
                cur.execute(command)
                # A temporary table used for executing a join.
                command = (
                    """
                    CREATE TABLE "temp" (
                      "show_title" varchar,
                      "music_video" varchar,
                      "release_date" varchar,
                      "type_of_show" varchar,
                      "episode_title" varchar,
                      "season_number" int,
                      "episode_number" int,
                      "suspended" varchar,
                      "release_year" varchar,
                      "end_year" varchar
                    );
                    """
                )
                cur.execute(command)
                # Puts the data in the temporary table.
                execute_values(cur,
                               "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, release_year, end_year) VALUES %s",
                               data)
                # Joins the data of the shows and their ratings.
                command = """
                                SELECT DISTINCT temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended, temp.end_year, ratings.distribution, ratings.amount_of_votes, ratings.rating
                                FROM temp
                                LEFT JOIN ratings
                                ON temp.show_title = ratings.show_title
                                AND temp.release_date = ratings.release_date
                                WHERE temp.end_year IS NOT NULL AND temp.release_date <> '????' AND ratings.episode_title IS NULL AND ratings.season_number IS NULL AND ratings.episode_number IS NULL
                                """
                cur.execute(command)
                data = cur.fetchall()
                # Deletes the temporary table.
                command = (
                    """
                    DROP TABLE temp
                    """
                )
                cur.execute(command)
                print("Got all the data needed for the show table")
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_show(show):
    print("Started inserting process")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                # A temporary table used for linking the rating of a show to the show.
                command = (
                    """
                    CREATE TABLE temp (
                        "temp_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
                        "show_title" varchar,
                        "release_date" varchar,
                        "release_year" varchar,
                        "type_of_show" varchar,
                        "suspended" bool,
                        "end_year" varchar,
                        "distribution" varchar,
                        "amount_of_votes" int,
                        "rating" float
                    )
                    """
                )
                cur.execute(command)
                # Inserts the data into the temporary table.
                execute_values(cur,"INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, end_year, distribution, amount_of_votes, rating) VALUES %s", show)
                # Alters the rating table for linking with the temporary table.
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
                command = "SELECT distribution, amount_of_votes, rating, temp_id  FROM temp"
                cur.execute(command)
                data = cur.fetchall()
                print("Inserting the data in the rating table")
                execute_values(cur, "INSERT INTO rating (distribution, amount_of_votes, rating, temp_id) VALUES %s", data)
                print("Getting the data for the show table")
                command = """
                                SELECT rating.rating_id, temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended, temp.end_year
                                FROM temp
                                INNER JOIN rating
                                ON rating.temp_id = temp.temp_id
                                """
                cur.execute(command)
                data = cur.fetchall()
                print("Inserting data in show table")
                execute_values(cur,
                               "INSERT INTO show (rating_id, show_title, release_date,release_year, type_of_show, suspended, end_year) VALUES %s",
                               data)
                # Alters the rating table for the deletion of the temporary table.
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
                # Deletes the temporary table.
                command = (
                    """
                    DROP TABLE temp
                    """
                )
                cur.execute(command)
                print("Inserted data in the show and rating table")
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
                print("Getting all data needed for the episode table from staging database")
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                # Selects the data for all the episodes of the shows in the movies.csv file.
                command = """
                                SELECT movies.show_title, movies.release_date, movies.release_year, movies.type_of_show, movies.suspended, movies.episode_title, movies.season_number, movies.episode_number, ratings.distribution, ratings.amount_of_votes, ratings.rating
                                FROM movies 
                                LEFT JOIN ratings
                                ON movies.show_title = ratings.show_title
                                AND movies.release_date = ratings.release_date
                                AND movies.episode_title = ratings.episode_title
                                AND movies.season_number = ratings.season_number
                                AND movies.episode_number = ratings.episode_number
                                WHERE (movies.end_year IS NULL) AND (movies.release_date IS NOT NULL) AND ((movies.episode_title IS NOT NULL OR movies.season_number IS NOT NULL) OR movies.episode_number IS NOT NULL)
                                """
                cur.execute(command)
                data = cur.fetchall()
                print("Got all the data needed for the episode table")
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_episode(episode):
    print("Started inserting process")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                # A temporary table for linking the episode and show table.
                command = (
                    """
                    CREATE TABLE temp (
                        "show_title" varchar,
                        "release_date" varchar,
                        "release_year" varchar,
                        "type_of_show" varchar,
                        "suspended" bool,
                        "episode_name" varchar,
                        "season_number" int,
                        "episode_number" int,
                        "distribution" varchar,
                        "amount_of_votes" int,
                        "rating" float
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, episode_name, season_number, episode_number, distribution, amount_of_votes, rating) VALUES %s",
                               episode)
                # Links the data of the episode to the correct show
                command = """
                                                                SELECT temp.*, show.show_id
                                                                FROM temp
                                                                LEFT JOIN show
                                                                ON temp.show_title = show.show_title
                                                                AND temp.release_date = show.release_date
                                                                """
                cur.execute(command)
                data = cur.fetchall()
                # Deletes the table, data has been retrieved.
                command = (
                    """
                    DROP TABLE temp
                    """
                )
                cur.execute(command)
                # A temporary table for the linking of episode, show and rating.
                command = (
                    """
                    CREATE TABLE temp (
                        "temp_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
                        "show_title" varchar,
                        "release_date" varchar,
                        "release_year" varchar,
                        "type_of_show" varchar,
                        "suspended" bool,
                        "episode_name" varchar,
                        "season_number" int,
                        "episode_number" int,
                        "distribution" varchar,
                        "amount_of_votes" int,
                        "rating" float,
                        "show_id" int 
                    )
                    """
                )
                cur.execute(command)
                # Puts the data in the temporary table.
                execute_values(cur,
                               "INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, episode_name, season_number, episode_number, distribution, amount_of_votes, rating, show_id) VALUES %s",
                               data)
                # Alters the rating table for linking with the temporary table.
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
                command = "SELECT distribution, amount_of_votes, rating, temp_id  FROM temp"
                cur.execute(command)
                data = cur.fetchall()
                print("Inserting the data in the rating table")
                execute_values(cur,
                               "INSERT INTO rating (distribution, amount_of_votes, rating, temp_id) VALUES %s",
                               data)
                print("Getting data for episode table")
                command = """
                                               SELECT rating.rating_id, temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended, temp.show_id, temp.episode_name, temp.season_number, temp.episode_number
                                               FROM temp
                                               INNER JOIN rating
                                               ON rating.temp_id = temp.temp_id
                                               WHERE temp.show_id IS NOT NULL 
                                               """
                cur.execute(command)
                data = cur.fetchall()
                print("Inserting data in episode table")
                execute_values(cur,
                               "INSERT INTO episode (rating_id, show_title, release_date, release_year, type_of_show, suspended, show_id, episode_name, season_number, episode_number) VALUES %s",
                               data)
                # Alters the rating table for the deletion of the temporary table.
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
                # Deletes the temporary table.
                cur.execute(command)
                command = (
                    """
                    DROP TABLE temp
                    """
                )
                cur.execute(command)
                print("Inserted data in the episode and rating table")
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
                print("Getting all data needed for the show_info table from staging database")
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                # Selects the data of all the movies  in the movies.csv file.
                command = """
                SELECT movies.show_title, movies.release_date, movies.release_year, movies.type_of_show, movies.suspended, ratings.distribution, ratings.amount_of_votes, ratings.rating
                FROM movies 
                LEFT JOIN ratings
                ON movies.show_title = ratings.show_title
                AND movies.release_date = ratings.release_date
                WHERE movies.episode_title is NULL AND movies.season_number IS NULL AND movies.episode_number IS NULL AND movies.end_year IS NULL 
                """
                cur.execute(command)
                data = cur.fetchall()
                print("Got all the data needed for the show_info table")
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_showinfo(show_info):
    print("Started inserting process")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                # A temporary table for the linking of show_info and rating.
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
                cur.execute(command)
                execute_values(cur,"INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, distribution, amount_of_votes, rating) VALUES %s", show_info)
                # Alters the rating table for linking with the temporary table.
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
                command = "SELECT distribution, amount_of_votes, rating, temp_id  FROM temp"
                cur.execute(command)
                data = cur.fetchall()
                print("Inserting the data in the rating table")
                execute_values(cur, "INSERT INTO rating (distribution, amount_of_votes, rating, temp_id) VALUES %s", data)

                print("Getting data for show_info table")
                command = """
                                SELECT rating.rating_id, temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended
                                FROM temp
                                INNER JOIN rating
                                ON rating.temp_id = temp.temp_id
                                """
                cur.execute(command)
                data = cur.fetchall()
                print("Inserting data in show_info table")
                execute_values(cur,
                               "INSERT INTO show_info (rating_id, show_title, release_date,release_year, type_of_show, suspended) VALUES %s",
                               data)
                # Alters the rating table for the deletion of the temporary table.
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
                # Deletes the temporary table.
                command = (
                    """
                    DROP TABLE temp
                    """
                )
                cur.execute(command)
                print("Inserted data in the show_info and rating table")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()

