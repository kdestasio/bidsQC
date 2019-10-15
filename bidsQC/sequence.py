from typing import Mapping


class Sequence:
    def __init__(self, name: str, files: Mapping[str, int]):
        self.name = name
        self.files = files

    def get_filecount(self) -> int:
        filecount = 0
        if len(self.files.values()) > 0:
            filecount = sum(self.files.values())

        return filecount
