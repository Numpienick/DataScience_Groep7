class DataSet:
    regex = ""
    file = ""

    def __init__(self):
        self.regex = self.regex
        self.file = self.file

    def print(self):
        print(self.regex, self.file)


class Actor(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actors"


class Actress(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "actresses"


class Cinematographer(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "cinematographers"


class Country(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<CountriesOfOrigin>\w.+)"
        self.file = "countries"


class Director(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "((?:(?P<LastName>.+?)\,\s)?(?P<FirstName>.+?)|\t\t\t)\t(\"(?P<SeriesTitle>(?!\t).+?)\"|(?P<Title>(?!\t).+?))\s\((?P<ReleaseDate>.+?)\)(?:\s)?(?:\{((?P<EpisodeName>(?!\{).+?)(?:\s\(\#(?P<Season>[0-9]{1,})\.(?P<Episode>[0-9]{1,})\))?)\}\s)?(?:\((?P<ShowType>[TVG]{1,2})\))?(?:.+?\((?P<Voicing>voice)\))?(?:.+?\((?P<Archive>archive footage)\))?(?:.+?\((?P<PlayedAs>as\s.*)\))?(?:.+?\((?P<Uncredited>uncredited)\))?(?:\{\{(?P<Suspended>SUSPENDED)\}\})?(?:.+?\[((?P<Role>.+?)(?:\(segment\s\"(?P<Segment>.+?)\"\))?)\])?(?:.+?\<(?P<Position>[0-9]{1,})\>)?"
        self.file = "directors"


class Genre(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = ""
        self.file = "genres"


class Movie(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#|\{).+?(?= \()|(?!\(\#|\{).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\s)?(?:(?P<Suspended>\{\{SUSPENDED\}\}))?(?:\0+?)?(?:\s+?)?(?P<ReleaseYear>\d{4}|\?{4})(?:-(?P<EndYear>\d{4}|\?{4}))?"
        self.file = "movies"


class Plot(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "(MV[\s\S]*?-------------------------------------------------------------------------------)"
        self.file = "plot"


class Rating(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = "\s*?(?P<Distribution>[0-9\.*]{10})\s+?(?P<Votes>\d+)\s+?(?P<Rating>.\d\.\d)\s+?(?P<Title>.*?)\s+?\((?P<Year>\d{4}.*?)\)\s+?((?:{.*})?)((?:\(.*\))?)"
        self.file = "ratings"


class RunningTime(DataSet):
    def __init__(self):
        super().__init__()
        self.regex = ""
        self.file = "running-times"
