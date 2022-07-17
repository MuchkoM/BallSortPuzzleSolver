import copy

from solver.palette import Palette
from solver.field import Field

from solver.utils import colored_text, get_alpha


class FieldPrinter:
    def __init__(self, field: Field, palette: Palette = None):
        self.field = field
        self.palette = palette

    def lines_normalizer(self, array, row_num):
        work_array = copy.deepcopy(array)

        for val in work_array:
            cur_num = len(val)
            if cur_num != row_num:
                for i in range(row_num - cur_num):
                    val.append(' ')

        lines = []
        for i in range(row_num):
            lines.append([])

        for i, col in enumerate(work_array):
            for j, el in enumerate(col):
                lines[row_num - j - 1].append(el)

        return lines

    def print(self, header: str = None, footer: str = None):
        lines = self.lines_normalizer(self.field.field, self.field.dimension)

        if header:
            print(header)

        for line in lines:
            symbols = []
            for symbol in line:
                if isinstance(symbol, int):
                    if self.palette:
                        symbols.append(colored_text(self.palette.get_color_by_index(symbol), get_alpha(symbol)))
                    else:
                        symbols.append(symbol)
                else:
                    symbols.append(symbol)
            print(*symbols, sep=' | ')
        if footer:
            print(footer)


if __name__ == '__main__':
    from examples.level297.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    field_printer = FieldPrinter(field, palette)
    field_printer.print()
