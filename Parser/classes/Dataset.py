class DataSet:
    clean_file_regex = r""
    regex = r""
    file = ""
    seperator = ""

    def __init__(self):
        self.regex = self.regex
        self.file = self.file
        self.clean_file_regex = self.clean_file_regex
        self.seperator = self.seperator

    def print(self):
        print(self.regex, self.file)

    def section_data(self, file):
        return ""

    def get_table(self):
        return ""

    def insert_table(self, data):
        return ""
