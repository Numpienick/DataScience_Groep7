from psycopg2.extras import execute_values

from Parser.DbConnector import connect
from Parser.classes.Dataset import DataSet


class Actress(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<nick_name>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<last_name>[\S ]+?)?, )?(?P<first_name>[\S ]+?)[^ \S]+|(?:\t\t\t))\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)(?:\s+?\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:(?:(?:(?:\s+)?\[(?:(?P<character_name>[^\[{()}\]]+?))(?:(?=\(|\{)|\)|\}|\])+)|(?:(?:\s+)?(?:\(|\{|\[)(?:(?:as (?P<also_known_as>[^)}\]]+?))|(?P<segment>segment[^)}\]]*?)|(?P<voice_actor>voice[^)}\]]*?)|(?P<scenes_deleted>scenes deleted)|(?P<credit_only>credit only)|(?P<archive_footage>archive footage)|(?P<uncredited>uncredited)|(?P<rumored>rumored)|(?P<motion_capture>motion capture)|(?:[^)}\]]+?))(?:\)|\}|\])+))+)?(?:\s+<(?P<role_position>[0-9]{1,})\>)?"
        self.file = "actresses"
        self.clean_file_regex = r"-{4}\s+?-{6}\s+(?P<data>[\s\S]+?(?=-{77}))"

    def get_table(self):
        print("Getting actresses from staging")
        try:
            conn = connect("staging")
            with conn:
                with conn.cursor() as cur:
                        cur.execute("SELECT DISTINCT * from actresses")
                        data = cur.fetchall()
                        return data
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()

    def insert_table(self, role):
        print("Inserting role")

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
                            suspended bool,
                            character_name varchar,
                            also_known_as varchar,
                            segment varchar,
                            voice_actor varchar,
                            scenes_deleted varchar,
                            credit_only varchar,
                            archive_footage varchar,
                            uncredited varchar,
                            rumored varchar,
                            motion_capture varchar,
                            role_position int,
                            female bool
                        )
                        """
                    )
                    cur.execute(command)
                    execute_values(cur,
                                   "INSERT INTO temp (nick_name, last_name, first_name, show_title, music_video, "
                                   "release_date, type_of_show, episode_title, season_number, episode_number, suspended, "
                                   "character_name, also_known_as, segment, voice_actor, scenes_deleted, credit_only, "
                                   "archive_footage, uncredited, rumored, motion_capture, role_position, female) VALUES "
                                   "%s",
                                   role)
                    command = """
                              SELECT show_info.show_info_id, temp.nick_name, temp.last_name, temp.first_name, temp.character_name, temp.segment, temp.voice_actor, temp.scenes_deleted, temp.credit_only, temp.archive_footage, temp.uncredited, temp.rumored, temp.motion_capture, temp.role_position, temp.female
                              FROM temp
                              LEFT JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date
                              """
                    cur.execute(command)
                    data = cur.fetchall()
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, character_name, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored, motion_capture, role_position, female) VALUES %s",
                                   data)
                    command = "DROP TABLE temp"
                    cur.execute(command)
                    print("did it")
        except Exception as err:
            raise err
        finally:
            if conn:
                conn.close()