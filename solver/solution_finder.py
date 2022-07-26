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

    def get_next_possible_way(self):
        cols = []
        for i, col in self.current.enumerate:
            col_len = len(col)
            cols.append((i, col, col_len, all_equal(col) if col_len > 2 else False))

        res = []
        for src_index, src_column, src_len, is_equal in cols:
            if src_len == 0:
                continue
            if (src_len == self.dimension or src_len == self.dimension - 1) and is_equal:
                continue
            for des_index, des_column, des_len, _ in cols:
                if src_index == des_index:
                    continue
                if des_len == self.dimension:
                    continue
                if not ((des_len > 0 and des_column[-1] == src_column[-1]) or (des_len == 0)):
                    continue
                if des_len == 0 and is_equal:
                    continue
                if (des_index, src_index, src_column[-1]) in self.way:
                    continue
                res.append((src_index, des_index, src_column[-1]))
        return res

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
                self.solved_way = self.way.copy
            return

        if self.solved_way and (len(self.way) > len(self.solved_way)):
            return

        if self.visited.is_known(self.current, self.way):
            return

        for src_index, des_index, element in self.get_next_possible_way():
            self.way.push((src_index, des_index, element))
            self.current.move(src_index, des_index)

            self.inner_solve()

            self.current.move(des_index, src_index)
            self.way.pop()


if __name__ == "__main__":
    from examples.const import field_arr, palette_arr

    field, palette = Field(field_arr), Palette(palette_arr)
    solver = SolutionFinder(field)

    start = datetime.now()
    solver.solve()
    duration = datetime.now() - start

    solution_printer = SolutionPrinter(field, solver.solved_way, palette)
    solution_printer.build()
    solution_printer.print_way()

    print(duration)
