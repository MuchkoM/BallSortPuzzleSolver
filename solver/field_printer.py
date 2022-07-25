from __future__ import annotations

import io
import sys
from typing import List, Tuple

from solver.field import Field
from solver.palette import Palette
from solver.utils import colored_text, get_alpha, print2d, map2d


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


class FieldPrinter:
    def __init__(self, field: Field, palette: Palette = None):
        self.field = field
        self.palette = palette
        self.field_filler = ' | '
        self.header_filler = '   '
        self.header_empty = ' '
        self.field_empty = ' '

        self.src_header_filler = '↑'
        self.des_header_filler = '↓'

    def prepare_header(self, src, des, el) -> List[str]:
        header_arr = [self.header_empty] * self.field.column
        header_arr[src] = colored_text(self.palette.get_color_by_index(el), self.src_header_filler)
        header_arr[des] = colored_text(self.palette.get_color_by_index(el), self.des_header_filler)

        return header_arr

    def print(self, header: Tuple[int, int, int] | str | None = None, footer: str | None = None, stream=sys.stdout):
        str_io = io.StringIO()

        def el_transform(element):
            if isinstance(element, int) and self.palette:
                return colored_text(self.palette.get_color_by_index(element), get_alpha(element))

            return element or self.field_empty

        transformed_field_array = self.field.get_transformed_field_array()
        transformed_field_array = map2d(el_transform, transformed_field_array)

        if header:
            if isinstance(header, tuple):
                print(self.header_filler.join(self.prepare_header(*header)), file=str_io)
            else:
                print(header, file=str_io)

        print2d(transformed_field_array, self.field_filler, str_io)

        if footer:
            print(footer, file=str_io)
        print(str_io.getvalue(), file=stream, end='')


if __name__ == '__main__':
    from examples.level297.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    field_printer = FieldPrinter(field, palette)
    field_printer.print(header=(1, 12, 0), footer='Step 1')
