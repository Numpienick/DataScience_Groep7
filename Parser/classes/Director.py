import os
from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Actor import Actor
from Parser.classes.Dataset import DataSet


class Director(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<nick_name>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<last_name>[\S ]+?)?, )?(?P<first_name>[\S ]+?)[^ \S]+|(?:\t\t\t))\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|(?<=\").+?(?=\")|.+(?= \([\d?]))\"?(?:\s\((?P<music_video>Music Video)?\))?(?:\s\((?P<release_date>\d[^?]+?)\)|\?{4}(?:.+?)?\))?(?:\s\((?P<type_of_show>TV|V|VG)\))?(?:\s\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \(#)|(?!\(\#|\{).+?(?=\}))?))?(?:\})?\s?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:(?:(?:\s+)?\((?:(?P<type_of_director>[^)]*?(?:director)|(?:directed)[^)]*?)|(?:as (?P<also_known_as>[^)]+?))|(?P<segment>segment[^)]*?)|(?P<voice_actor>voice[^)]*?)|(?P<scenes_deleted>scenes deleted)|(?P<credit_only>credit only)|(?P<archive_footage>archive footage)|(?P<uncredited>uncredited)|(?P<rumored>rumored)|(?:[^)]+?))\))+)?"
        self.file = "directors"
        self.clean_file_regex = r"-{4}\s+?-{6}\s+(?P<data>[\s\S]+?(?=-{77}))"

    def get_table(self):
        print("Getting directors from staging")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT DISTINCT * from directors WHERE episode_title IS NULL AND episode_number IS NULL AND season_number IS NULL")
                    data = cur.fetchall()
                return data
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, director):
        print("Inserting director")

        try:
            conn = connect("final")
            with conn:
                with conn.cursor() as cur:
                    command = (
                        """
                        CREATE TABLE temp (
                            nick_name varchar,
                            last_name varchar,
                            first_name varchar,
                            show_title varchar,
                            music_video varchar,
                            release_date varchar,
                            type_of_show varchar,
                            episode_title varchar,
                            season_number int,
                            episode_number int,
                            suspended varchar,
                            type_of_director varchar,
                            also_known_as varchar,
                            segment varchar,
                            voice_actor varchar,
                            scenes_deleted varchar,
                            credit_only varchar,
                            archive_footage varchar,
                            uncredited varchar,
                            rumored varchar
                        )
                        """
                    )
                    cur.execute(command)
                    execute_values(cur,
                                   "INSERT INTO temp (nick_name, last_name, first_name, show_title, music_video, "
                                   "release_date, type_of_show, episode_title, season_number, episode_number, suspended, "
                                   "type_of_director, also_known_as, segment, voice_actor, scenes_deleted, "
                                   "credit_only, archive_footage, uncredited, rumored) VALUES "
                                   "%s",
                                   director)
                    cur.execute(
                        "SELECT nick_name, last_name, first_name, type_of_director, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored from temp")
                    temp = cur.fetchall()
                    execute_values(cur,
                                   "INSERT INTO director (nick_name, last_name, first_name, type_of_director, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                                   temp)

                    command = """
                              SELECT DISTINCT show_info.show_info_id, director.director_id
                              FROM temp
                              INNER JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              INNER JOIN director
                              ON temp.first_name = director.first_name
                              AND temp.last_name = director.last_name
                              AND temp.nick_name = director.nick_name
                              """
                    cur.execute(command)
                    data = cur.fetchall()

                    execute_values(cur, "INSERT INTO show_info_director (show_info_id, director_id) VALUES %s", data)
                    Director.insert_also_known_as(cur)

                    command = "DROP TABLE temp"
                    cur.execute(command)
                    print("\033[1;32mFinished inserting Director to Director and Person and show_info_director")

        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    @classmethod
    def insert_also_known_as(cls, cur):
        return "" #Commented out because the same issue as episodes, foreign key + inheritance limitation?
        print("Inserting known as")

        command = """
                  SELECT DISTINCT temp.also_known_as
                  FROM temp
                  WHERE temp.also_known_as IS NOT NULL
                  """
        cur.execute(command)
        also_known_as = cur.fetchall()
        execute_values(cur, "INSERT INTO also_known_as (also_known_as) VALUES %s", also_known_as)

        command = """
                  SELECT DISTINCT director.person_id, also_known_as.also_known_as_id
                  FROM temp
                  INNER JOIN also_known_as
                  ON temp.also_known_as = also_known_as.also_known_as
                  INNER JOIN director
                  ON temp.last_name = director.last_name
                  AND temp.first_name = director.first_name                         
                  """
        cur.execute(command)
        also_known_as_link = cur.fetchall()
        execute_values(cur, "INSERT INTO person_also_known_as (person_id, also_known_as_id) VALUES %s", also_known_as_link)