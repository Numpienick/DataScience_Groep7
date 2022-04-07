import os

from playsound import playsound
from psycopg2.extras import execute_values
from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class Movie(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|(?<=\").+?(?=\")|.+(?= \([\d?]))\"?(?:\s\((?P<music_video>Music Video)?\))?(?:\s\((?P<release_date>\d[^?]+?)\)|\?{4}(?:.+?)?\))?(?:\s\((?P<type_of_show>TV|V|VG)\))?(?:\s\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \(#)|(?!\(\#|\{).+?(?=\}))?))?(?:\})?\s?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?\0*?\s*?(?:(?P<release_year>\d{4})|\?{4})(?:-(?P<end_year>\d{4}|\?{4}))?"
        self.file = "movies"

    def get_table(self):
        print("Getting movies from staging")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    print("Getting all data needed for the show_info table from staging database")
                    command = """
                                                SELECT DISTINCT(movies.show_title), movies.release_date, movies.release_year, movies.type_of_show, movies.suspended, ratings.distribution, ratings.amount_of_votes, ratings.rating
                                                FROM movies 
                                                LEFT JOIN ratings
                                                ON movies.show_title = ratings.show_title
                                                AND movies.release_date = ratings.release_date
                                                WHERE movies.episode_title IS NULL AND movies.season_number IS NULL AND movies.episode_number IS NULL AND movies.end_year IS NULL
                                                """
                    cur.execute(command)
                    data = cur.fetchall()
                    print("Data Length: " + str(len(data)))
                    print("Got all the data needed for the show_info table")
                    return data

        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, show_info):
        print("Started inserting process show_info table")
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
                    execute_values(cur,
                                   "INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, distribution, amount_of_votes, rating) VALUES %s",
                                   show_info)
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
                    print("Data Length: " + str(len(data)))
                    print("Inserting the data in the rating table")
                    execute_values(cur, "INSERT INTO rating (distribution, amount_of_votes, rating, temp_id) VALUES %s",
                                   data)

                    print("Getting data for show_info table")
                    command = """
                                            SELECT rating.rating_id, temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended
                                            FROM temp
                                            INNER JOIN rating
                                            ON rating.temp_id = temp.temp_id
                                            """
                    cur.execute(command)
                    data = cur.fetchall()
                    print("Data Length: " + str(len(data)))
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
