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


def get_col_prop(column, dim):
    length = len(column)
    top = dim - length
    middle = get_top_equal(column, length)
    bot = length - middle
    return middle, bot, top


def get_file():
    files = glob.glob('./examples/level298/*.jpeg')
    files.sort(key=lambda x: os.path.getctime(x))

    return files[-1]


def prior_possible_ways(ways, dimension):
    ways_t = tuple(ways)
    if len(ways_t) > 1:
        known_props = dict()

        def get_props(index, col):
            if index in known_props:
                return known_props[index]
            else:
                res = known_props[index] = get_col_prop(col, dimension)
                return res

        def sort_conditions(x):
            src_index, src_column, des_index, des_column, _ = x
            ms, bs, ts = get_props(src_index, src_column)
            md, bd, td = get_props(des_index, des_column)
            return -ts, -td

        return sorted(ways_t, key=sort_conditions)
    else:
        return ways_t
