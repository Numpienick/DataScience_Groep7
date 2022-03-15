class Movie:
    initialRegex = "(?s).+?(?=(\"))(.+?(?=(--------------------------------------------------------------------------------)))"
    regex = ""
    file = "movies"


class Actor:
    regex = ""
    file = "actors"


class Country:
    initialRegex = "[^==============]*$"
    file = "countries"

class Plot:
    initialRegex = "MV[\s\S]*?-------------------------------------------------------------------------------"
    file = "plot"

class Rating:
    initialRegex = "\s*?(?P<Distribution>[0-9\.*]{10})\s+?(?P<Votes>\d+)\s+?(?P<Rating>.\d\.\d)\s+?(?P<Title>.*?)\((?P<Year>\d{4}).*?\)|\s+?\((?P<Platform>(?:TV)|(?:V)|(?:VG))\)\s*?|{(?P<Episode>.*?)}"
    file = "ratings"
