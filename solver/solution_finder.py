from datetime import datetime

from solver.field import Field
from solver.palette import Palette
from solver.solution_printer import SolutionPrinter
from solver.utils import all_equal
from solver.visited_fields import VisitedFields
from solver.way import Way


class SolutionFinder:
    def __init__(self, field: Field):
        self.visited: VisitedFields = None
        self.way: Way = None
        self.current: Field = None
        self.solved_way: Way = None
        self.field = field
        self.dimension = field.dimension

    @property
    def is_solved(self):
        return self.solved_way and len(self.solved_way) > 0

    def filter_source_cols(self, cols):
        def filter_cond(x):
            src_index, src_column = x

            src_len = len(src_column)
            if src_len == 0:
                return False

            if (src_len == self.dimension or src_len == self.dimension - 1) and all_equal(src_column):
                return False

            return True

        return filter(filter_cond, cols)

    def filter_des_cols(self, current_enum, src_index, src_column):
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

            if (des_index, src_index, src_column[-1]) in self.way:
                return False

            return True

        return filter(filter_cond, current_enum)

    def get_next_possible_way(self):
        for src_index, src_column in self.filter_source_cols(self.current.enumerate):
            for des_index, des_column in self.filter_des_cols(self.current.enumerate, src_index, src_column):
                yield src_index, src_column, des_index, des_column, src_column[-1]

    def solve(self):
        self.current = self.field.copy
        self.way = Way()
        self.visited = VisitedFields()
        self.solved_way = None
        try:
            self.inner_solve()
        except KeyboardInterrupt:
            print('Process was interrupted')
            pass

    def inner_solve(self):
        if self.current.is_solved:
            if self.way.is_better(self.solved_way):
                print(len(self.way))
                self.solved_way = self.way.copy
            return

        if self.solved_way and (len(self.way) > len(self.solved_way)):
            return

        if self.visited.is_known(self.current, self.way):
            return

        for src_index, src_column, des_index, des_column, element in self.get_next_possible_way():
            self.way.push((src_index, des_index, element))
            self.current.move(src_index, des_index)

            self.inner_solve()

            self.current.move(des_index, src_index)
            self.way.pop()


if __name__ == "__main__":
    from examples.level2__.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    solver = SolutionFinder(field)

    start = datetime.now()
    solver.solve()
    duration = datetime.now() - start

    if solver.is_solved:
        solution_printer = SolutionPrinter(field, solver.solved_way, palette)
        solution_printer.print_way()

        print(solver.solved_way)
        print(len(solver.visited))
        print(duration)
