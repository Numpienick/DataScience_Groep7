import re
import time
import itertools as it

class DataSet:
    cleanFileRegex = r""
    regex = r""
    file = ""
    seperator = ""

    def __init__(self):
        self.regex = self.regex
        self.file = self.file
        self.cleanFileRegex = self.cleanFileRegex
        self.seperator = self.seperator

    def print(self):
        print(self.regex, self.file)

    def sectionData(self, file):
        return ""

class Actor(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<nick_name>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<last_name>[\S ]+?)?, )?(?P<first_name>[\S ]+?)[^ \S]+|(?:\t\t\t))\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)(?:\s+?\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:(?:(?:(?:\s+)?\[(?:(?P<character_name>[^\[{()}\]]+?))(?:(?=\(|\{)|\)|\}|\])+)|(?:(?:\s+)?(?:\(|\{|\[)(?:(?:as (?P<also_known_as>[^)}\]]+?))|(?P<segment>segment[^)}\]]*?)|(?P<voice_actor>voice[^)}\]]*?)|(?P<scenes_deleted>scenes deleted)|(?P<credit_only>credit only)|(?P<archived_footage>archive footage)|(?P<uncredited>uncredited)|(?P<rumored>rumored)|(?P<motion_capture>motion capture)|(?:[^)}\]]+?))(?:\)|\}|\])+))+)?(?:\s+<(?P<role_position>[0-9]{1,})\>)?"
        self.file = "actors"
        self.cleanFileRegex = r"-{4}\s+?-{6}\s+(?P<data>[\s\S]+?(?=-{77}))"


class Actress(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<nick_name>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<last_name>[\S ]+?)?, )?(?P<first_name>[\S ]+?)[^ \S]+|(?:\t\t\t))\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)(?:\s+?\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:(?:(?:(?:\s+)?\[(?:(?P<character_name>[^\[{()}\]]+?))(?:(?=\(|\{)|\)|\}|\])+)|(?:(?:\s+)?(?:\(|\{|\[)(?:(?:as (?P<also_known_as>[^)}\]]+?))|(?P<segment>segment[^)}\]]*?)|(?P<voice_actor>voice[^)}\]]*?)|(?P<scenes_deleted>scenes deleted)|(?P<credit_only>credit only)|(?P<archived_footage>archive footage)|(?P<uncredited>uncredited)|(?P<rumored>rumored)|(?P<motion_capture>motion capture)|(?:[^)}\]]+?))(?:\)|\}|\])+))+)?(?:\s+<(?P<role_position>[0-9]{1,})\>)?"
        self.file = "actresses"
        self.cleanFileRegex = r"-{4}\s+?-{6}\s+(?P<data>[\s\S]+?(?=-{77}))"


class Cinematographer(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<nick_name>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<last_name>[\S ]+?)?, )?(?P<first_name>[\S ]+?)[^ \S]+|(?:\t\t\t))\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)(?:\s+?\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:(?:(?:\s+)?\((?:(?P<type_of_cinematographer>[^)]*?(?:director)|(?:directed)[^)]*?)|(?:videos? (?P<video>[^)]+?)?)|(?:as (?P<also_known_as>[^)]+?))|(?P<segment>segment[^)]*?)|(?P<voice_actor>voice[^)]*?)|(?P<scenes_deleted>scenes deleted)|(?P<credit_only>credit only)|(?P<archived_footage>archive footage)|(?P<uncredited>uncredited)|(?P<rumored>rumored)|(?P<motion_capture>motion capture)|(?:[^)]+?))\))+)?"
        self.file = "cinematographers"
        self.cleanFileRegex = r"-{4}\s+?-{6}\s+(?P<data>[\s\S]+?(?=-{77}))"


class Country(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?\s*(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\0*?\s+?(?P<countries_of_origin>\w.+)"
        self.file = "countries"


class Director(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<nick_name>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<last_name>[\S ]+?)?, )?(?P<first_name>[\S ]+?)[^ \S]+|(?:\t\t\t))\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)(?:\s+?\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:(?:(?:\s+)?\((?:(?P<type_of_director>[^)]*?(?:director)|(?:directed)[^)]*?)|(?:videos? (?P<video>[^)]+?)?)|(?:as (?P<also_known_as>[^)]+?))|(?P<segment>segment[^)]*?)|(?P<voice_actor>voice[^)]*?)|(?P<scenes_deleted>scenes deleted)|(?P<credit_only>credit only)|(?P<archived_footage>archive footage)|(?P<uncredited>uncredited)|(?P<rumored>rumored)|(?P<motion_capture>motion capture)|(?:[^)]+?))\))+)?"
        self.file = "directors"
        self.cleanFileRegex = r"-{4}\s+?-{6}\s+(?P<data>[\s\S]+?(?=-{77}))"


class Genre(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?\s*(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\0*?\s+?(?P<Genre>\w.+)"
        self.file = "genres"


class Movie(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+?(?= \(Music Video\) \([\d?])|.+?(?=\")|.+?(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.*?)(?:[?\/I]*?)?\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s)?(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\0*?\s*?(?P<release_year>\d{4}|\?{4})(?:-(?P<end_year>\d{4}|\?{4}))?"
        self.file = "movies"


class Plot(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:(?:MV:\s)\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?)?(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\s+PL: (?:(?P<plot>[\s\S]+?)(?=(?:\nBY:|\n-{79})|\n\n\n)(?:\nBY:\s(?P<written_by>.+))?)"
        self.file = "plot"
        self.seperator = "-------------------------------------------------------------------------------"

    def sectionData(self, file):
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


class Rating(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\s*?(?P<distribution>[0-9\.*]{10})\s+?(?P<amount_of_votes>\d+)\s+?(?P<rating>\d+?\.\d)\s+(?:\")?\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s)?(?:\{\{?(?P<suspended>SUSPENDED)\}\})?\s*"
        self.file = "ratings"


class RunningTime(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|.+(?=\")|.+(?= \([\d?]))\"?\s\((?:(?P<music_video>Music Video)?\)\s\()?(?P<release_date>.+?)\)\s+?(?:\((?P<type_of_show>TV|V|VG)\))?(?:\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s)?(?:\{\{?(?P<suspended>SUSPENDED)\}\})?(?:\s+)?(?:(?P<country>.+?)?:)?(?P<running_time>\d+)(?:(?:(?:\s+)?\((?:(?P<commercial>[^)]*?(?:C|c)ommercials?[^)]*?)|(?P<episodes>[^)]*?(?:E|e)pisodes?[^)]*?)|(?P<season>[^)]*?(?:S|s)easons?[^)]*?)|(?:(?P<release_year>[\d\?]{4})-(?P<end_year>[\d\?]{4}))|(?P<fps>[^)]*?fps)|(?P<festival>[^(]*?(?:F|f)estival)|(?P<cut>[^)]*?(?:C|c)ut[^)]*?)|(?P<market>[^)]*?(?:M|m)arket)|(?P<print>[^)]*(?:P|p)rint)|(?P<approximated>approx\.)|(?:[^)]+?))\))+)?"
        self.file = "running-times"
