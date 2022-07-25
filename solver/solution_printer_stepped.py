from __future__ import annotations

import os
import sys

from solver.field import Field
from solver.palette import Palette
from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionFinder
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
    def __init__(self, field: Field, way: Way, palette: Palette | None = None):
        self.print_step_list = SolutionPrinter(field, way, palette)
        self.print_step_list.build()

        self.commands = Commands({
            '\n': self.forward,
            ' ': self.backward,
            'N': self.end
        })

        self.index = 0

    def interact(self, stream=sys.stdout):
        self.being()

        self.print(stream)

        self.commands.wait_input()

    def increment(self):
        if self.index != len(self.print_step_list) - 1:
            self.index += 1

    def decrement(self):
        if self.index != 0:
            self.index -= 1

    def being(self):
        self.index = 0

    def forward(self, stream=sys.stdout):
        self.increment()
        self.print(stream)

    def backward(self, stream=sys.stdout):
        self.decrement()
        self.print(stream)

    def print(self, stream=sys.stdout):
        os.system('clear')
        print(self.print_step_list[self.index], end='', file=stream)

    def end(self, stream=sys.stdout):
        print('Exit', file=stream)
        return True


if __name__ == '__main__':
    analyzer = ScreenshotCV('../examples/level3/2022-07-20 18.31.28.jpg')
    analyzer.analyze()

    solver = SolutionFinder(analyzer.field)
    solver.solve()

    if solver.is_solved:
        solution_printer = SolutionPrinterStepped(analyzer.field, solver.solved_way, analyzer.palette)
        solution_printer.interact()
    else:
        print('Solution is not found')
