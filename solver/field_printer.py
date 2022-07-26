from __future__ import annotations

import io
import sys
from typing import List, Tuple

from solver.field import Field
from solver.palette import Palette
from solver.utils import colored_text, get_alpha, print2d, map2d, print1d


def split_at_index(array, split_index):
    return array[:split_index], array[split_index:]


def get_transformed_field_array(field, dimension):
    res_list: List[List[None | int]] = [[None] * len(field) for _ in range(dimension)]

    for i, col in enumerate(field):
        for j, el in enumerate(col):
            res_list[dimension - j - 1][i] = el

    return res_list


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

    def get_output_el(self, el, symbol):
        if self.palette:
            return colored_text(self.palette.get_color_by_index(el), symbol)
        else:
            return symbol

    def prepare_header_arr(self, src, des, el) -> List[str]:
        header_arr = [self.header_empty] * self.field.column
        header_arr[src] = self.get_output_el(el, self.src_header_filler)
        header_arr[des] = self.get_output_el(el, self.des_header_filler)
        return header_arr

    def splatted_header(self, header, split_index):
        header_arr = ['', '']
        if isinstance(header, tuple):
            header_arr = split_at_index(self.prepare_header_arr(*header), split_index)
        elif isinstance(header, str):
            header_arr[0] = header
        return header_arr

    def print(self, header: Tuple[int, int, int] | str | None = None, footer: str | None = None, stream=sys.stdout):
        str_io = io.StringIO()
        div, mod = divmod(self.field.column, 2)
        split_index = div + mod

        def el_transform(element):
            if element is None:
                return element or self.field_empty
            return self.get_output_el(element, get_alpha(element))

        for i, (part, header_part) in enumerate(zip(split_at_index(self.field, split_index),
                                                    self.splatted_header(header, split_index))):
            transformer_field_part = get_transformed_field_array(part, self.field.dimension)
            transformer_field_part = map2d(el_transform, transformer_field_part)
            pre = '  ' if i == 1 and mod == 1 else ''
            if isinstance(header, tuple):
                print1d(header_part, self.header_filler, str_io, pre)
            else:
                print(header_part, file=str_io)
            print2d(transformer_field_part, self.field_filler, str_io, pre)
        if footer:
            print(footer, file=str_io)
        else:
            print(file=str_io)
        print(str_io.getvalue(), file=stream, end='')


if __name__ == '__main__':
    from examples.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    field_printer = FieldPrinter(field, palette)
    print('Output 1')
    field_printer.print(header=(1, 2, 0), footer='Step 1')
    print('Output 2')
    field_printer.print(footer='Solved')
    print('Output 3')
    field_printer.print(header='Solution', footer='Solved')
    print('Output 4')
    field_printer.print()
    print('End')
