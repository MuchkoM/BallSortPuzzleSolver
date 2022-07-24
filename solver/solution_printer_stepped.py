import io
import os

from solver.field import Field
from solver.field_printer import FieldPrinter
from solver.palette import Palette
from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionFinder
from solver.utils import colored_text, get_file, getch
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


class PrintStepList:
    def __init__(self, way: Way, field: Field, palette: Palette):
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


class SolutionPrinterStepped:
    def __init__(self, field: Field, way: Way, palette: Palette):
        self.print_step_list = PrintStepList(way, field, palette)
        self.print_step_list.build()

        self.commands = Commands({
            '\n': self.forward,
            ' ': self.backward,
            'N': self.end
        })

        self.index = 0

    def interact(self):
        self.index = 0

        self.print()

        self.commands.wait_input()

    def forward(self):
        if self.index != len(self.print_step_list) - 1:
            self.index += 1

        self.print()

    def backward(self):
        if self.index != 0:
            self.index -= 1

        self.print()

    def print(self):
        os.system('clear')
        print(self.print_step_list[self.index], end='')

    def end(self):
        print('Exit')
        return True


if __name__ == '__main__':
    analyzer = ScreenshotCV(get_file())
    analyzer.analyze()

    solver = SolutionFinder(analyzer.field)
    solver.solve()

    if solver.is_solved:
        solution_printer = SolutionPrinterStepped(analyzer.field, solver.solved_way, analyzer.palette)
        solution_printer.interact()
    else:
        print('Solution is not found')
