import copy
from typing import Tuple, List

from solver.field import Field


class Way:
    def __init__(self, way=None):
        self.way: List[Tuple[int, int, int]] = way or []

    def push(self, source: Tuple[int, int, int]):
        self.way.append(source)

    def pop(self):
        self.way.pop()

    def copy(self):
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.way)

    def __str__(self):
        return str(self.way)

    def __repr__(self):
        return str(self.way)


class Ways:
    def __init__(self):
        self.arr = []

    def add(self, way: Way):
        self.arr.append(way.copy())

    def is_solved(self):
        return len(self.arr) > 0

    def fast_way(self):
        return sorted(self.arr, key=lambda x: len(x))[0]


class VisitedFields:
    def __init__(self):
        self.visited = set()

    def is_visited(self, current: Field):
        return current in self.visited

    def visit(self, current: Field):
        self.visited.add(current)
