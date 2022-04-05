from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class Plot(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:(?:MV:\s)\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?)?(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\s+PL: (?:(?P<plot>[\s\S]+?)(?=(?:\nBY:|\n-{79})|\n\n\n)(?:\nBY:\s(?P<written_by>.+))?)"
        self.file = "plot"
        self.seperator = "-------------------------------------------------------------------------------"

    def section_data(self, file):
        # works, but takes ages to parse so for now it's disabled
        return ""
        # startTime = time.perf_counter()
        # print(f"\nStarting sectioning of {self.file}'s data")
        # titleRegex = r"(?:MV:\s)(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?"
        # bodyRegex = r"PL: (?P<Plot>[\s\S]+?)(?=(?:\nBY:|\n-{79})|\n\nPL: )\n(?P<By>BY:\s.+)"
        # sections = list()
        # txt = str()
        # for key, group in it.groupby(file, lambda line: line.startswith(self.seperator)):
        #     if not key:
        #         section = str()
        #         for line in group:
        #             section += line
        #         sections.append(section)
        # for section in sections:
        #     title = re.search(titleRegex, section, re.M)
        #     bodies = re.findall(bodyRegex, section, re.M)
        #     for body in bodies:
        #         txt += f"{self.seperator}\n{title.group()}\nPL: {''.join(body)}\n\n"
        #     # FOR getMatches IF NEEDED IN FUTURE
        #     # txt = txt.split(seperator)
        #     # for section in txt:
        #     #     if section != "":
        #     #         match = re.search(dataType.regex, section, re.M)
        #     #         if match is not None:
        #     #             matches.append(match)
        # endTime = time.perf_counter()
        # print(f"Done sectioning {self.file} in {endTime - startTime:0.04f} seconds")
        # return txt

    def get_table(self):
        print("Getting plot from staging")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM plot")
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
                    command = "DROP TABLE temp"
                    cur.execute(command)
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

                    execute_values(cur,
                                   "INSERT INTO genre (genre_name) VALUES %s",
                                   data)

                    command = """
                              SELECT show_info.show_info_id, plot.plot_id
                              FROM temp
                              LEFT JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              JOIN plot
                              ON temp.plot = plot.plot
                              AND temp.written_by = plot.written_by
                              """
                    cur.execute(command)
                    link_table = cur.fetchall()
                    execute_values(cur,
                                   "INSERT INTO show_info_plot (show_info_id, genre_id) VALUES %s",
                                   link_table)
                    command = "DROP TABLE temp"
                    cur.execute(command)
                    print("did it")
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()
