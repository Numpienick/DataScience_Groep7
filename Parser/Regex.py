class DataSet:
    cleanFileRegex = ""
    regex = ""
    file = ""

    def __init__(self):
        self.regex = self.regex
        self.file = self.file
        self.cleanFileRegex = self.cleanFileRegex

    def print(self):
        print(self.regex, self.file)


class Actor(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?:(?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actors"
        self.cleanFileRegex = "----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Actress(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(?:, )?(?P<NickName>\'[\S ]+?\'|^\"[\S ]+?\")?(?:,)?(?: )?(?:(?:(?P<LastName>[\S ]+?)?, )?(?P<FirstName>[\S ]+?)[^ \S]+?|(?:\t\t\t))(?:\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?: )?(?:\{(?:(?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[(?:(?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actresses"
        self.cleanFileRegex = "----			------\s+(?P<data>[\s\S]+?(?=-----------------------------------------------------------------------------))"


class Cinematographer(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "cinematographers"
        self.cleanFileRegex = ""


class Country(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<CountriesOfOrigin>\w.+)"
        self.file = "countries"
        self.cleanFileRegex = ""


class Director(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "directors"
        self.cleanFileRegex = ""


class Genre(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = ""
        self.file = "genres"
        self.cleanFileRegex = ""


class Movie(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = r"(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<ReleaseYear>\d{4}|\?{4})(?:-(?P<EndYear>\d{4}|\?{4}))?"
        self.file = "movies"
        self.cleanFileRegex = ""


class Plot(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(MV[\s\S]*?-------------------------------------------------------------------------------)"
        self.file = "plot"
        self.cleanFileRegex = ""


class Rating(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "\s*?(?P<Distribution>[0-9\.*]{10})\s+?(?P<Votes>\d+)\s+?(?P<Rating>.\d\.\d)\s+?(?P<Title>.*?)\s+?\((?P<Year>\d{4}.*?)\)\s+?((?:{.*})?)((?:\(.*\))?)"
        self.file = "ratings"
        self.cleanFileRegex = ""


class RunningTime(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = ""
        self.file = "running-times"
        self.cleanFileRegex = ""
