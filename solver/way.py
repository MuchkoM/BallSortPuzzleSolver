import copy
from typing import Tuple, List


class Way:
    def __init__(self, way=None):
        self.way: List[Tuple[int, int, int]] = way or []

    def push(self, source: Tuple[int, int, int]):
        self.way.append(source)

    def pop(self):
        self.way.pop()

    def __getitem__(self, item):
        return self.way[item]

    @property
    def copy(self):
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.way)

    def __str__(self):
        return str(self.way)

    def __repr__(self):
        return str(self.way)

    def __contains__(self, item):
        return item in self.way

    def is_better(self, solved_way):
        return not solved_way or (len(self) < len(solved_way))
