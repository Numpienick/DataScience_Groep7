from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class Country(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|(?<=\").+?(?=\")|.+(?= \([\d?]))\"?(?:\s\((?P<music_video>Music Video)?\))?(?:\s\((?P<release_date>\d[^?]+?)\)|\?{4}(?:.+?)?\))?(?:\s\((?P<type_of_show>TV|V|VG)\))?(?:\s\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \(#)|(?!\(\#|\{).+?(?=\}))?))?(?:\})?\s?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?\0*?\s+?(?P<countries_of_origin>\w.+)"
        self.file = "countries"

    def get_table(self):
        print("Getting countries")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM countries WHERE episode_title IS NULL AND episode_number IS NULL AND season_number IS NULL")
                    data = cur.fetchall()
                    print("Data Length: " + str(len(data)))
                    return data

        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, countries):
        print("Inserting countries")

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
                            countries_of_origin varchar
                        )
                        """
                    )
                    cur.execute(command)
                    execute_values(cur,
                                   "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, countries_of_origin) VALUES %s",
                                   countries)

                    cur.execute("SELECT DISTINCT countries_of_origin FROM temp")
                    data = cur.fetchall()
                    print("Data Length: " + str(len(data)))

                    execute_values(cur,
                                   "INSERT INTO country (country_name) VALUES %s",
                                   data)

                    command = """
                              SELECT DISTINCT show_info.show_info_id, country.country_id
                              FROM temp
                              INNER JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              INNER JOIN country
                              ON temp.countries_of_origin = country.country_name
                              """
                    cur.execute(command)
                    link_table = cur.fetchall()
                    execute_values(cur, "INSERT INTO show_info_country (show_info_id, country_id) VALUES %s", link_table)
                    command = "DROP TABLE temp"
                    cur.execute(command)
                    print("\033[1;32mFinished inserting Country to Country and show_info_country")
        except Exception as err:
            #playsound(os.path.abspath('./assets/fail.wav'))
            raise err
        finally:
            if conn:
                conn.close()
