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
        self.regex = r"(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:\0+?)?(?:\s+?)?\s+(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actors"
        self.cleanFileRegex = r"----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Actress(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:\0+?)?(?:\s+?)?\s+(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actresses"
        self.cleanFileRegex = r"----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Cinematographer(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:\0+?)?(?:\s+?)?\s+(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "cinematographers"
        self.cleanFileRegex = "----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Country(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<CountriesOfOrigin>\w.+)"
        self.file = "countries"
        self.cleanFileRegex = r""


class Director(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:\0+?)?(?:\s+?)?\s+(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "directors"
        self.cleanFileRegex = "----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


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
        self.regex = r"\s*?(?P<Distribution>[0-9\.*]{10})\s+?(?P<Votes>\d+)\s+?(?P<Rating>.\d\.\d)\s+?(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?"
        self.file = "ratings"
        self.cleanFileRegex = r""


class RunningTime(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?P<Title>.*?)\((?P<Year>[0-9\/I\?]{4,8})\)\s+?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>{{SUSPENDED}}))?(?:\0+?)?(?:\s+?)?\s*(?:\()?(?P<Showtype>(?:TV|V|VG))?(?:\))?\s*?(?P<Country>(?:\w.*?\:)?)(?P<RunningTime>\d{1,4})\s+?(?:\()?(?P<Approx>(?:approx.)?)(?:\)\s*\()?(?P<Season>(?:\w*\s*season)?)(?:\)\s*\()?(?P<Commercials>(?:\w*\s*commercials)?)(?:\)\s*\()?(?P<TotalEpisodes>(?:\d{1,3}\s*episodes|\d{1,3}\s*Episodes)?)(?:\)\s*\()?(?P<FPS>(?:\d*\s*fps)?)(?:\)\s*\()?(?P<Version>(?:[a-zA-Z0-9\s]*?version)?)(?:\)\s*\()?(?P<Parts>(?:\d{0,3}\s*parts|\w*\s*parts)?)(?:\)\s*\()?(?P<Festival>(?:[a-zA-z\s]*?Festival)?)(?:\)\s*\()?(?P<Cut>(?:[a-zA-z'\s]*?cut|[a-zA-z'\s]*?Cut)?)(?:\)\s*\()?(?P<Market>(?:[a-zA-z\s]*?Market)?)(?:\)\s*\()?(?P<Print>(?:\w*\s*print)?)(?:\))?"
        self.file = "running-times"
        self.cleanFileRegex = r""
