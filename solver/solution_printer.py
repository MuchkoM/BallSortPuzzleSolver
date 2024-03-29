from __future__ import annotations

import io
from typing import Tuple

from solver.field import Field
from solver.field_printer import FieldPrinter
from solver.palette import Palette
from solver.way import Way


class SolutionPrinter:
    def __init__(self, field: Field, way: Way, palette: Palette | None = None):
        self.field = field
        self.way = way
        self.palette = palette

        self.step_list = []

    def build(self):
        current = self.field.copy

        self.step_list = []

        for i, (src, des, el) in enumerate(self.way):
            self._add_step(
                field=current,
                header=(src, des, el),
                footer='Step {} out of {}'.format(i + 1, len(self.way))
            )

            current.move(src, des)
        self._add_step(
            field=current,
            header=' ',
            footer='Solved in {} steps'.format(len(self.way))
        )

    def _add_step(self, field: Field, header: Tuple[int, int, int] | str | None = None, footer: str | None = None):
        printer = FieldPrinter(field, self.palette)
        str_io = io.StringIO()
        printer.print(header, footer, str_io)

        self.step_list.append(str_io.getvalue())

    def __len__(self):
        return len(self.step_list)

    def __getitem__(self, item: int):
        return self.step_list[item]

    def print_way(self):
        for step in self.step_list:
            print(step, end='')


if __name__ == '__main__':
    from examples.const import way_arr, field_arr, palette_arr

    field, way, palette = Field(field_arr), Way(way_arr), Palette(palette_arr)

    solution_printer = SolutionPrinter(field, way, palette)
    solution_printer.build()
    solution_printer.print_way()
