from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class RunningTime(DataSet):
    def __init__(self):
        super().__init__() #TODO: parts uit part group halen
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s)?(?:\{\{?(?P<suspended>SUSPENDED)\}\})?(?:\s+)?(?:(?P<country>.+?)?:)?(?P<running_time>\d+)(?:(?:(?:\s+)?\((?:(?P<commercial>[^)]*?(?:C|c)ommercials?[^)]*?)|(?P<episodes>[^)]*?(?:E|e)pisodes?[^)]*?)|(?P<season>[^)]*?(?:S|s)easons?[^)]*?)|(?:(?P<release_year>[\d\?]{4})-(?P<end_year>[\d\?]{4}))|(?P<fps>[^)]*?fps)|(?P<festival>[^(]*?(?:F|f)estival)|(?P<cut>[^)]*?(?:C|c)ut[^)]*?)|(?P<market>[^)]*?(?:M|m)arket)|(?P<print>[^)]*(?:P|p)rint)|(?P<approximated>approx\.)|(?:[^)]+?))\))+)?"
        self.file = "running-times"

    def get_table(self):
        print("Getting running times from staging")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * from running_times")
                    data = cur.fetchall()
                return data
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, running_times):
        print("Inserting running times")

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
                            country varchar,
                            running_times integer,
                            including_commercials varchar,
                            amount_of_episodes varchar,
                            season varchar,
                            release_year varchar,
                            end_year varchar,
                            fps varchar,
                            festival varchar,
                            cut varchar,
                            market varchar,
                            print varchar,
                            approximated varchar
                        )
                        """
                    )
                    cur.execute(command)
                    execute_values(cur,
                                   "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, country, video, running_times, including_commercials, amount_of_episodes, season, release_year, end_year, fps, festival, cut, market, print, approximated) VALUES "
                                   "%s",
                                   running_times)
                    cur.execute(
                        "SELECT show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, country, video, running_times, including_commercials, amount_of_episodes, season, release_year, end_year, fps, festival, cut, market, print, approximated from temp")
                    temp = cur.fetchall()
                    execute_values(cur,
                                   "INSERT INTO running_times (nick_name, last_name, first_name, type_of_director, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                                   temp)

                    command = """
                              SELECT show_info.show_info_id, director.director_id
                              FROM temp
                              LEFT JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              JOIN director
                              ON temp.first_name = director.first_name
                              AND temp.last_name = director.last_name
                              AND temp.nick_name = director.nick_name
                              """
                    cur.execute(command)
                    data = cur.fetchall()

                    execute_values(cur,
                                   "INSERT INTO show_info_director (show_info_id, director_id) VALUES %s",
                                   data)

                    command = "DROP TABLE temp"
                    cur.execute(command)
                    print("did it")
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()
