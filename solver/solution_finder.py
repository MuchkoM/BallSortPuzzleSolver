from solver.palette import Palette
from solver.field import Field
from solver.solution_printer import SolutionPrinter
from solver.way import Way, VisitedFields
from solver.utils import all_equal


class SolutionBuilder:
    def __init__(self, field: Field):
        self.field = field
        self.dimension = field.dimension

    def get_top_equal(self, col):
        for i in range(2, self.dimension):
            if len(col) >= i and col[-i:].count(col[-1]) == i:
                return i
        return 0

    def get_source_cols(self, current):
        def filter_cond(x):
            src_index, src_column = x

            src_len = len(src_column)
            if src_len == 0:
                return False

            if src_len == self.dimension and all_equal(src_column):
                return False

            return True

        def sorter(x):
            return self.get_top_equal(x[1]), len(x[1])

        return sorted(filter(filter_cond, enumerate(current.field)), key=sorter)

    def get_des_cols(self, current, src_index, src_column):
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

        def sorter(x):
            return -self.get_top_equal(x[1]), - len(x[1])

        return sorted(filter(filter_cond, enumerate(current.field)), key=sorter)

    def get_indexes_and_element(self, current):
        for src_index, src_column in self.get_source_cols(current):
            des_arr = self.get_des_cols(current, src_index, src_column)
            for des_index, des_column in des_arr:
                yield src_index, des_index, src_column[-1]

    def _solve(self, way: Way, current: Field, visited: VisitedFields) -> bool:
        visited.push(current)
        for src_index, des_index, element in self.get_indexes_and_element(current):
            way.push((src_index, des_index, element))
            current.move(src_index, des_index)

            if not visited.is_visited(current):
                if not current.is_solved():
                    result = self._solve(way, current, visited)
                    if result:
                        return True
                else:
                    return True

            current.move(des_index, src_index)
            way.pop()

    def solve(self):
        current = self.field.copy()
        way = Way()
        visited = VisitedFields()

        return self._solve(way, current, visited), way


if __name__ == "__main__":
    from examples.level2__.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    solver = SolutionBuilder(field)

    is_solved, way = solver.solve()
    print(way.way)

    solution_printer = SolutionPrinter(field, way, palette)
    solution_printer.print_way()
    print(len(way.way))
