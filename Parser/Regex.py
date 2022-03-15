class Movie:
    initialRegex = "(?s).+?(?=(\"))(.+?(?=(--------------------------------------------------------------------------------)))"
    file = "movies"

class Actor:
    regex = ""
    file = "actors"

class Country:
    initialRegex = "^(.*)==============([\s\S]*)*"
    file = "countries"
