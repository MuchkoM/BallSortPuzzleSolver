from __future__ import annotations

import os
import sys

from solver.field import Field
from solver.palette import Palette
from solver.solution_printer import SolutionPrinter
from solver.utils import getch
from solver.way import Way


class Commands:
    def __init__(self, mapping):
        self.mapping = mapping

    def wait_input(self):
        while True:
            key = getch().upper()
            if key in self.mapping:
                if self.mapping[key]():
                    break


class SolutionPrinterStepped:
    def __init__(self, solution_printer: SolutionPrinter):
        self.solution_printer = solution_printer
        self.commands = Commands({
            '\n': self.forward,
            ' ': self.backward,
            'N': self.end
        })

        self.index = 0

    def interact(self, stream=sys.stdout):
        self.begin()

        os.system('clear')
        self.print(stream)

        self.commands.wait_input()

    def increment(self):
        if self.index != len(self.solution_printer) - 1:
            self.index += 1

    def decrement(self):
        if self.index != 0:
            self.index -= 1

    def begin(self):
        self.index = 0

    def forward(self, stream=sys.stdout):
        self.increment()
        os.system('clear')
        self.print(stream)

    def backward(self, stream=sys.stdout):
        self.decrement()
        os.system('clear')
        self.print(stream)

    def print(self, stream=sys.stdout):
        print(self.solution_printer[self.index], end='', file=stream)

    def end(self, stream=sys.stdout):
        print('Exit', file=stream)
        return True

    def __hash__(self):
        return hash(self.solution_printer.field)


if __name__ == '__main__':
    from examples.const import field_arr, way_arr, palette_arr

    field, way, palette = Field(field_arr), Way(way_arr), Palette(palette_arr)

    solution_printer = SolutionPrinter(field, way, palette)
    solution_printer.build()

    solution_printer_stepper = SolutionPrinterStepped(solution_printer)
    solution_printer_stepper.interact()
