from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class Genre(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?\s*(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\0*?\s+?(?P<Genre>\w.+)"
        self.file = "genres"

    def get_table(self):
        print("Getting genres")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM genres")
                    data = cur.fetchall()
                    return data

        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, genres):
        print("Inserting genres")

        try:
            conn = connect("final")
            with conn:
                with conn.cursor() as cur:
                    command = (
                        """
                        CREATE TABLE temp (
                            show_title varchar,
                            music_video varchar,
                            release_date varchar,
                            type_of_show varchar,
                            episode_title varchar,
                            season_number int,
                            episode_number int,
                            suspended varchar,
                            genre varchar
                        )
                        """
                    )
                    cur.execute(command)
                    execute_values(cur,
                                   "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, genre) VALUES %s",
                                   genres)

                    cur.execute("SELECT DISTINCT genre FROM temp")
                    data = cur.fetchall()

                    execute_values(cur,
                                   "INSERT INTO genre (genre_name) VALUES %s",
                                   data)

                    command = """
                              SELECT show_info.show_info_id, genre.genre_id
                              FROM temp
                              LEFT JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              JOIN genre
                              ON temp.genre = genre.genre
                              """
                    cur.execute(command)
                    link_table = cur.fetchall()
                    execute_values(cur,
                                   "INSERT INTO show_info_genre (show_info_id, genre_id) VALUES %s",
                                   link_table)
                    print("did it")
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()
