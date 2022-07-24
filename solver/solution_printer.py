import io

from solver.field import Field
from solver.field_printer import FieldPrinter
from solver.palette import Palette
from solver.utils import colored_text
from solver.way import Way


# def printer(array, row_num=None, next_line=7, header1="", header2=""):
#     if row_num is None:
#         row_num = len(array[0])
#
#     lines = lines_normalizer(array, row_num)
#
#     for line in lines:
#         print(*line, sep=' | ')
#
#
# def lines_normalizer(array, row_num):
#     work_array = copy.deepcopy(array)
#
#     for val in work_array:
#         cur_num = len(val)
#         if cur_num != row_num:
#             for i in range(row_num - cur_num):
#                 val.append(' ')
#
#     lines = []
#     for i in range(row_num):
#         lines.append([])
#
#     for i, col in enumerate(work_array):
#         for j, el in enumerate(col):
#             lines[row_num - j - 1].append(el)
#
#     return lines
#
#
# def flask_to_str(source, divider):
#     div, mod = divmod(source, divider)
#     return f'{mod + 1}{"↓" if div == 1 else "↑"}'
#
#
# def print_split(lines, row_num, divider, header=False, stream=sys.stdout):
#     splatted = [[], []]
#     for group in splatted:
#         for i in range(row_num):
#             group.append([])
#
#     for i, line in enumerate(lines):
#         for j, el in enumerate(line):
#             if j < divider:
#                 splatted[0][i].append(el)
#             else:
#                 splatted[1][i].append(el)
#
#     for cur_lines in splatted:
#         for i, line in enumerate(cur_lines):
#             print(*transform_line(line), sep='   ' if header & (i == 0) else ' | ', file=stream)
#
#
# def print_solution(start, way, stream=sys.stdout):
#     curr_start = copy.deepcopy(start)
#     col_num = len(curr_start)
#     row_num = len(curr_start[0])
#     divider = col_num // 2
#
#     for i, step in enumerate(way):
#         s, t, c = step
#         print('From {} to {}. Step {} from {}'.format(
#             flask_to_str(s, divider),
#             flask_to_str(t, divider),
#             i + 1,
#             len(way)
#         ), file=stream)
#
#         header = []
#         for j in range(col_num):
#             cur_symbol = ' '
#             if j == s:
#                 cur_symbol = '↑'
#             if j == t:
#                 cur_symbol = '↓'
#             header.append(cur_symbol)
#
#         lines = lines_normalizer(curr_start, row_num)
#         lines.insert(0, header)
#
#         print_split(lines, row_num + 1, divider, header=True)
#
#         push(curr_start, s, t)
#     print("\nSolved:", file=stream)
#     lines = lines_normalizer(curr_start, row_num)
#     print_split(lines, row_num, divider)


class SolutionPrinter:
    def __init__(self, field: Field, way: Way, palette: Palette):
        self.field = field
        self.way = way
        self.palette = palette

        self.step_list = []

    def build(self):
        current = self.field.copy

        self.step_list = []

        for i, (src, des, el) in enumerate(self.way):
            self.add_step(
                field=current,
                header=self.header(src, des, el),
                footer='Step {} out {}'.format(i + 1, len(self.way))
            )

            current.move(src, des)
        self.add_step(
            field=current,
            header=' ',
            footer='Solved in {} steps'.format(len(self.way))
        )

    def add_step(self, field, header, footer):
        printer = FieldPrinter(field, self.palette)
        str_io = io.StringIO()
        printer.print(header, footer, str_io)

        self.step_list.append(str_io.getvalue())

    def header(self, src, des, el):
        header_arr = [' '] * self.field.column
        header_arr[src] = colored_text(self.palette.get_color_by_index(el), '↑')
        header_arr[des] = colored_text(self.palette.get_color_by_index(el), '↓')

        return '   '.join(header_arr)

    def __len__(self):
        return len(self.step_list)

    def __getitem__(self, item):
        return self.step_list[item]

    def print_way(self):
        for step in self.step_list:
            print(step)


if __name__ == '__main__':
    from examples.level2__.const import way_arr, field_arr, palette_arr

    field = Field(field_arr)
    way = Way(way_arr)
    palette = Palette(palette_arr)

    solution_printer = SolutionPrinter(field, way, palette)
    solution_printer.build()
    solution_printer.print_way()
