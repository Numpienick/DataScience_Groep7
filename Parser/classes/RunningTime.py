from Parser.classes.Dataset import DataSet


class RunningTime(DataSet):
    def __init__(self):
        super().__init__() #TODO: parts uit part group halen
        self.regex = r"""\"?(?P<show_title>.+(?= \(Music Video\) \([\d?])|(?<=\").+?(?=\")|.+(?= \([\d?]))\"?(?:\s\((?P<music_video>Music Video)?\))?(?:\s\((?P<release_date>\d[^?]+?)\)|\?{4}(?:.+?)?\))?(?:\s\((?P<type_of_show>TV|V|VG)\))?(?:\s\{(?P<episode_title>(?:(?!\(\#|\{).+?(?= \(#)|(?!\(\#|\{).+?(?=\}))?))?(?:\})?\s?(?:\(\#(?P<season_number>\d+?)\.(?P<episode_number>\d+?)\)\})?(?:\s\{\{?(?P<suspended>SUSPENDED)\}\})?(?:\s+)?(?:(?P<country>.+?)?:)?(?P<running_time>\d+)(?:(?:(?:\s+)?\((?:(?P<including_commercials>[^)]*?(?:C|c)ommercials?[^)]*?)|(?P<amount_of_episodes>[^)]*?(?:E|e)pisodes?[^)]*?)|(?P<season>[^)]*?(?:S|s)easons?[^)]*?)|(?:(?P<release_year>[\d\?]{4})-(?P<end_year>[\d\?]{4}))|(?P<fps>[^)]*?fps)|(?P<festival>[^(]*?(?:F|f)estival)|(?P<cut>[^)]*?(?:C|c)ut[^)]*?)|(?P<market>[^)]*?(?:M|m)arket)|(?P<print>[^)]*(?:P|p)rint)|(?P<approximated>approx\.)|(?:[^)]+?))\))+)?"""
        self.file = "running-times"
