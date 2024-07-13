import glob
import math
import os
import sys
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
    return tuple(map(int, pixel))


def all_equal(col):
    first = col[0]
    for el in col:
        if el != first:
            return False
    return True


def get_file():
    files = glob.glob('*.jpeg')
    files.sort(key=lambda x: os.path.getctime(x))

    return files[-1]


def getch():
    import termios
    import tty
    fd = sys.stdin.fileno()
    orig = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)  # or tty.setraw(fd) if you prefer raw mode's behavior.
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, orig)


def map2d(callback, res):
    return [list(map(callback, x)) for x in res]


def print2d(array, joiner: str, stream, pre=''):
    for line in array:
        print1d(line, joiner, stream, pre)


def print1d(array, joiner: str, stream, pre=''):
    print(pre, file=stream, end='')
    print(*array, sep=joiner, file=stream)
