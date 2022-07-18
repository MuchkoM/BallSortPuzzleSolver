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


class VisitedFields:
    def __init__(self):
        self.visited = []

    def is_eq(self, ar1: Field, ar2: Field):
        if len(ar1.field) != len(ar2.field):
            return False
        for el1, el2 in zip(ar1.field, ar2.field):
            if el1 != el2:
                return False
        return True

    def is_visited(self, current: Field):
        for ar in self.visited:
            if self.is_eq(current, ar):
                return True
        return False

    def is_try_visit(self, current: Field) -> bool:
        if not self.is_visited(current):
            self.push(current)
        else:
            return True

    def push(self, current: Field):
        self.visited.append(current.copy())
