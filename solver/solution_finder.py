from datetime import datetime

from solver.field import Field
from solver.palette import Palette
from solver.solution_printer import SolutionPrinter
from solver.utils import all_equal
from solver.way import Way, VisitedFields, Ways


class SolutionBuilder:
    def __init__(self, field: Field):
        self.visited: VisitedFields = None
        self.way: Way = None
        self.current: Field = None
        self.ways: Ways = None
        self.field = field
        self.dimension = field.dimension
        self.reset()

    def is_solved(self):
        return self.ways.is_solved()

    def fast_way(self):
        return self.ways.fast_way()

    def reset(self):
        self.current = self.field.copy()
        self.way = Way()
        self.visited = VisitedFields()
        self.ways = Ways()

    def filter_source_cols(self, cols):
        def filter_cond(x):
            src_index, src_column = x

            src_len = len(src_column)
            if src_len == 0:
                return False

            if src_len == self.dimension and all_equal(src_column):
                return False

            return True

        return tuple(filter(filter_cond, cols))

    def filter_des_cols(self, cols, src_index, src_column):
        def filter_cond(x):
            des_index, des_column = x

            if src_index == des_index:
                return False

            des_len = len(des_column)

            if des_len == self.dimension:
                return False

            if not ((des_len > 0 and des_column[-1] == src_column[-1]) or (des_len == 0)):
                return False

            if des_len == 0 and all_equal(src_column):
                return False

            return True

        return tuple(filter(filter_cond, cols))

    def get_source_cols(self):
        return self.filter_source_cols(self.current.get_enumerate())

    def get_des_cols(self, src_index, src_column):
        return self.filter_des_cols(self.current.get_enumerate(), src_index, src_column)

    def get_indexes_and_element(self):
        for src_index, src_column in self.get_source_cols():
            for des_index, _ in self.get_des_cols(src_index, src_column):
                yield src_index, des_index, src_column[-1]

    def solve(self):
        if self.current.is_solved():
            self.ways.add(self.way)
            return
        if self.visited.is_visited(self.current):
            return
        self.visited.visit(self.current)

        for src_index, des_index, element in self.get_indexes_and_element():
            self.way.push((src_index, des_index, element))
            self.current.move(src_index, des_index)

            self.solve()

            self.current.move(des_index, src_index)
            self.way.pop()


if __name__ == "__main__":
    from examples.level2__.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    solver = SolutionBuilder(field)

    start = datetime.now()
    solver.solve()
    duration = datetime.now() - start

    if solver.is_solved():
        solution_printer = SolutionPrinter(field, solver.fast_way(), palette)
        solution_printer.print_way()

        print(len(solver.ways.arr), tuple(map(len, solver.ways.arr)))
        print(len(solver.visited.visited))
        print(duration)
