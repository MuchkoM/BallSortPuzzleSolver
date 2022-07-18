import copy
import itertools
from typing import List
from collections import Counter

from solver.utils import all_equal


class Field:
    def __init__(self, field_array: List[List[int]]):
        self.field: List[List[int]] = field_array
        self.dimension = len(field_array[0])
        self.column = len(field_array)

    def is_valid(self):
        flatter = list(itertools.chain.from_iterable(self.field))

        counter = Counter(flatter)

        return all_equal(counter.values())

    def is_solved(self):
        for el in self.field:
            is_equal = all_equal(el) and (len(el) == self.dimension or len(el) == 0)
            if not is_equal:
                return False
        return True

    def move(self, source, destination):
        self.field[destination].append(self.field[source].pop())

    def get_enumerate(self):
        return enumerate(self.field)

    def copy(self):
        return copy.deepcopy(self)


if __name__ == "__main__":
    from examples.level297.const import field_arr

    field_obj = Field(field_arr)
    print(field_obj.is_valid())
