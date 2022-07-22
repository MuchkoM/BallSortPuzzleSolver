from solver.field import Field
from solver.palette import Palette
from solver.way import Way
from solver.field_printer import FieldPrinter
from solver.utils import colored_text


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
    # todo add splitting by line top is higher
    def __init__(self, field: Field, way: Way, palette: Palette):
        self.palette = palette
        self.way = way.copy
        self.field = field.copy

    def print_way(self):
        current = self.field.copy
        field_printer = FieldPrinter(current, self.palette)
        for i, (src, des, el) in enumerate(self.way.way):
            field_printer.print(self.build_header(src, des, el), f'{i + 1}')
            current.move(src, des)
        field_printer.print(header=' ', footer=f'Solution is reachable in {len(self.way.way)} steps')

    def build_header(self, source, dest, el) -> str:
        header_arr = [' '] * self.field.column
        header_arr[source] = colored_text(self.palette.get_color_by_index(el), '↑')
        header_arr[dest] = colored_text(self.palette.get_color_by_index(el), '↓')
        return '   '.join(header_arr)


if __name__ == '__main__':
    from examples.level2__.const import way_arr, field_arr, palette_arr

    field = Field(field_arr)
    way = Way(way_arr)
    palette = Palette(palette_arr)

    solution_printer = SolutionPrinter(field, way, palette)
    solution_printer.print_way()
