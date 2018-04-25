# Establish classes

class TimePoint:
    def __init__(self, name: str, sequences: list):
        self.name = name
        self.sequences = sequences


class Sequence:
    def __init__(self, name: str, files: dict):
        self.name = name
        self.files = files

    def get_filecount(self):
        filecount = 0
        for key in self.files.keys():
            filecount = filecount + self.files[key]
        return filecount