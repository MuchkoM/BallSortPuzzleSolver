from solver.palette import Palette
from solver.field import Field
from solver.solution_printer import SolutionPrinter
from solver.way import Way, VisitedFields
from solver.utils import all_equal


class SolutionBuilder:
    def __init__(self, field: Field):
        self.visited: VisitedFields = None
        self.way: Way = None
        self.current: Field = None
        self.field = field
        self.dimension = field.dimension
        self.reset()

    def reset(self):
        self.current = field.copy()
        self.way = Way()
        self.visited = VisitedFields()

    def get_top_equal(self, col):
        for i in range(2, self.dimension):
            if len(col) >= i and col[-i:].count(col[-1]) == i:
                return i
        return 0

    def filter_source_cols(self, cols):
        def filter_cond(x):
            src_index, src_column = x

            src_len = len(src_column)
            if src_len == 0:
                return False

            if src_len == self.dimension and all_equal(src_column):
                return False

            return True

        return filter(filter_cond, cols)

    def prior_source_cols(self, cols):
        def sorter(x):
            _, column = x
            return self.get_top_equal(column), len(column)

        return sorted(cols, key=sorter)

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

        return filter(filter_cond, cols)

    def prior_des_cols(self, cols):
        def sorter(x):
            _, column = x
            return -self.get_top_equal(column), -len(column)

        return sorted(cols, key=sorter)

    def get_source_cols(self):
        return self.prior_source_cols(self.filter_source_cols(self.current.get_enumerate()))

    def get_des_cols(self, src_index, src_column):
        return self.prior_des_cols(self.filter_des_cols(self.current.get_enumerate(), src_index, src_column))

    def get_indexes_and_element(self):
        for src_index, src_column in self.get_source_cols():
            for des_index, _ in self.get_des_cols(src_index, src_column):
                yield src_index, des_index, src_column[-1]

    def solve(self) -> bool:
        if self.visited.is_try_visit(self.current):
            return False

        if self.current.is_solved():
            return True

        for src_index, des_index, element in self.get_indexes_and_element():
            self.way.push((src_index, des_index, element))
            self.current.move(src_index, des_index)

            if self.solve():
                return True

            self.current.move(des_index, src_index)
            self.way.pop()


if __name__ == "__main__":
    from examples.level297.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    solver = SolutionBuilder(field)

    if solver.solve():
        solution_printer = SolutionPrinter(field, solver.way, palette)
        solution_printer.print_way()
