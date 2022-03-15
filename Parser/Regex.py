class Movie:
    initialRegex = "(?:\")?(?P<ShowTitle>.+?)(?:\")?\s\((?P<ReleaseDateOrder>\d{4}(?:[^)]+?)?|\?{4}(?:.+?)?)\)\s+?(?:\((?P<ShowType>(?:TV)|(?:V)|(?:VG))\))?(?:\{(?P<EpisodeTitle>(?:(?!\(\#).+?(?= \()|(?!\(\#).+?(?=\}))?))?(?:\})?(?:\s)?(?:\(\#(?P<SeasonNumber>\d+?)\.(?P<EpisodeNumber>\d+?)\)\})?(?:\0+?)?(?:\s+?)?(?P<ReleaseYear>\d{4}|\?{4})(?:-(?P<EndYear>\d{4}|\?{4}))?"
    regex = ""
    file = "movies"


class Actor:
    regex = ""
    file = "actors"


class Country:
    initialRegex = "[^==============]*$"
    file = "countries"

class Plot:
    initialRegex = "(MV[\s\S]*?-------------------------------------------------------------------------------)"
    file = "plot"

class Rating:
    initialRegex = "\s*?(?P<Distribution>[0-9\.*]{10})\s+?(?P<Votes>\d+)\s+?(?P<Rating>.\d\.\d)\s+?(?P<Title>.*?)\s+?\((?P<Year>\d{4}.*?)\)\s+?((?:{.*})?)((?:\(.*\))?)"
    file = "ratings"
