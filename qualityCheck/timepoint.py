from typing import List
from sequence import Sequence


class TimePoint:
    def __init__(self, name: str, sequences: List[Sequence]):
        self.name = name
        self.sequences = sequences
