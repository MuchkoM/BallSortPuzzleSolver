import glob
import math
import os
from typing import Union, Tuple
from itertools import groupby


def colored_text_rgb(r, g, b, txt):
    return f"\033[38;2;{r};{g};{b}m{txt}\033[m"


def cie76(c1: Tuple[int, int, int], c2: Tuple[int, int, int]):
    return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2) + math.pow(c1[2] - c2[2], 2))


def colored_text(color: [int, int, int], text: Union[str, int]):
    b, g, r = color
    return colored_text_rgb(r, g, b, text)


def get_alpha(index: int):
    return chr(index + ord('A'))


def get_int_color(pixel):
    return int(pixel[0]), int(pixel[1]), int(pixel[2])


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def get_file():
    files = glob.glob('examples/level297/*.jpeg')
    files.sort(key=lambda x: os.path.getctime(x))

    return files[-1]
