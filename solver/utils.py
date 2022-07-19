import glob
import math
import os
from typing import Union, Tuple


def colored_text_rgb(r: int, g: int, b: int, txt: Union[str, int]):
    return f"\033[38;2;{r};{g};{b}m{txt}\033[m"


def cie76(c1: Tuple[int, int, int], c2: Tuple[int, int, int]):
    return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2) + math.pow(c1[2] - c2[2], 2))


def colored_text(color: [int, int, int], text: Union[str, int]):
    return colored_text_rgb(*reversed(color), text)


def get_alpha(index: int):
    return chr(index + ord('A'))


def get_int_color(pixel):
    return int(pixel[0]), int(pixel[1]), int(pixel[2])


def all_equal(col):
    first = col[0]
    for el in col:
        if el != first:
            return False
    return True


def get_top_equal(col, length):
    if length == 0:
        return 0
    for i in range(1, length):
        if col[-1 - i] != col[-1]:
            return i

    return length


def strange_top_equal(col, length):
    if length < 2:
        return 0
    if col[-1] == col[-2]:
        return 2
    else:
        return 0


def get_col_prop(column):
    length = len(column)
    top = -length
    middle = strange_top_equal(column, length)
    bot = top - middle
    return middle, bot, top


def get_file():
    files = glob.glob('examples/level297/*.jpeg')
    files.sort(key=lambda x: os.path.getctime(x))

    return files[-1]
