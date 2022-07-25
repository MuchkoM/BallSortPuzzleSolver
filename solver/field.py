from __future__ import annotations

import copy
from typing import List

from solver.utils import all_equal


class Field:
    def __init__(self, field_array: List[List[int]]):
        self.field: List[List[int]] = field_array
        self.dimension = len(field_array[0])
        self.column = len(field_array)

    @property
    def is_solved(self):
        for col in self.field:
            is_equal = (len(col) == self.dimension and all_equal(col)) or len(col) == 0
            if not is_equal:
                return False
        return True

    def move(self, source, destination):
        self.field[destination].append(self.field[source].pop())

    @property
    def enumerate(self):
        return enumerate(self.field)

    @property
    def copy(self):
        return copy.deepcopy(self)

    @property
    def tuple(self):
        return tuple(map(tuple, sorted(self.field)))

    def __repr__(self):
        return str(self.tuple)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __getitem__(self, item):
        return self.field[item]

    def __len__(self):
        return len(self.field)

    def __hash__(self):
        return hash(self.tuple)


if __name__ == "__main__":
    field_1 = Field([[1, 1, 1], [2, 3], [2, 2], [], []])
    field_1.t = 4
    field_2 = Field([[2, 3], [1, 1, 1], [], [2, 2], []])
    field_3 = Field([[1, 1, 1], [2, 3], [], [], [2, 2]])
    field_4 = Field([[1, 1, 1], [2, 3], [2], [2]])
    field_5 = Field([[1, 1, 1], [2, 3], [2, 2], [], []])
    field_5.t = 2

    print(field_1 == field_2)

    visited = {field_1}
    print(visited)

    visited.add(field_2)
    print(visited)

    visited.add(field_3)
    print(visited)

    visited.add(field_4)
    print(visited)

    visited.add(field_5)
    print(visited)

    print(field_5 in visited)
    obj = visited.intersection({field_5}).pop()
    visited.discard(field_5)
    print(obj.t)
    print(visited)

    visited = set()

    field_1.t = 'fake'
    visited.add(field_1)

    visited.discard(field_1)

    field_5.t = 'fake'
    visited.add(field_5)

    print(field_1 in visited)
    obj = {field_1}.intersection(visited).pop()
    visited.discard(field_1)
    print(obj is field_5)
    print(visited)
