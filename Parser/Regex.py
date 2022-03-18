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
        self.regex = r"(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?:(?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actors"
        self.cleanFileRegex = r"----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Actress(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?:(?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actresses"
        self.cleanFileRegex = r"----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Cinematographer(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "cinematographers"
        self.cleanFileRegex = r""


class Country(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<CountriesOfOrigin>\w.+)"
        self.file = "countries"
        self.cleanFileRegex = r""


class Director(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "directors"
        self.cleanFileRegex = r""


class Genre(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s)+(?P<Genre>.+)"
        self.file = "genres"
        self.cleanFileRegex = r""


class Movie(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<ReleaseYear>\d{4}|\?{4})(?:-(?P<EndYear>\d{4}|\?{4}))?"
        self.file = "movies"
        self.cleanFileRegex = r""


class Plot(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:(?:MV:\s)(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?)?\s+PL: (?:(?P<Plot>[\s\S]+?)(?=(?:\nBY:|\n-{79})|\n\n\n)(?:\nBY:\s(?P<By>.+))?)"
        self.file = "plot"
        self.cleanFileRegex = r""
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
        self.regex = r"\s*?(?P<Distribution>[0-9\.*]{10})\s+?(?P<Votes>\d+)\s+?(?P<Rating>.\d\.\d)\s+?(?P<Title>.*?)\s+?\((?P<Year>\d{4}.*?)\)\s+?((?:{.*})?)((?:\(.*\))?)"
        self.file = "ratings"
        self.cleanFileRegex = r""


class RunningTime(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r""
        self.file = "running-times"
        self.cleanFileRegex = r""
