from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class Plot(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:(?:MV:\s)\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|(?<=\").+?(?=\")|.+(?= \([\d?]))\"?(?:\s\((?P<music_video>Music Video)?\))?(?:\s\((?P<release_date>\d[^?]+?)\)|\?{4}(?:.+?)?\))?(?:\s\((?P<type_of_show>TV|V|VG)\))?(?:\s\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \(#)|(?!\(\#|\{).+?(?=\}))?))?(?:\})?\s?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?)?\s+PL: (?:(?P<plot>[\s\S]+?)(?=(?:\nBY:|\n-{79})|\n\n\n)(?:\nBY:\s(?P<written_by>.+))?)"
        self.file = "plot"
        self.seperator = "-------------------------------------------------------------------------------"

    def get_table(self):
        print("Getting plot from staging")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM plot WHERE episode_title IS NULL AND episode_number IS NULL AND season_number IS NULL")
                    data = cur.fetchall()
                    return data
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, plot):
        print("Inserting plot")

        try:
            conn = connect("final")
            with conn:
                with conn.cursor() as cur:
                    command = (
                        """
                        CREATE TEMP TABLE temp (
                            show_title varchar,
                            music_video varchar,
                            release_date varchar,
                            type_of_show varchar,
                            episode_title varchar,
                            season_number int,
                            episode_number int,
                            suspended varchar,
                            plot varchar,
                            written_by varchar
                        )
                        """
                    )
                    cur.execute(command)
                    execute_values(cur,
                                   "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, plot, written_by) VALUES %s",
                                   plot)

                    cur.execute("SELECT plot, written_by FROM temp")
                    data = cur.fetchall()

                    execute_values(cur, "INSERT INTO plot (plot, written_by) VALUES %s", data)

                    command = """
                              SELECT DISTINCT show_info.show_info_id, plot.plot_id
                              FROM temp
                              INNER JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              INNER JOIN plot
                              ON temp.plot = plot.plot
                              AND temp.written_by = plot.written_by
                              """
                    cur.execute(command)
                    link_table = cur.fetchall()
                    execute_values(cur, "INSERT INTO show_info_plot (show_info_id, plot_id) VALUES %s", link_table)
                    command = "DROP TABLE temp"
                    cur.execute(command)
                    print("\033[1;32mFinished inserting Plot to Plot and show_info_plot")
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()
