import copy
import sys


class Solved(Exception):
    pass


class Skip(Exception):
    pass


def push(arr, source, receiver):
    arr[receiver].append(arr[source].pop(-1))


def pop(arr, source, receiver):
    arr[source].append(arr[receiver].pop(-1))


def if_eq_column(column, n):
    return len(column) >= n and column[-n:].count(column[-1]) == n


def is_eq(ar1, ar2):
    if len(ar1) != len(ar2):
        return False
    for el1, el2 in zip(ar1, ar2):
        if el1 != el2:
            return False
    return True


def if_top_equal(column, n):
    return len(column) == n and column[-n:].count(column[-1]) == n and column[-1]


def printer(array, row_num=None, next_line=7, header1="", header2=""):
    if row_num is None:
        row_num = len(array[0])

    lines = lines_normalizer(array, row_num)

    for line in lines:
        print(*line, sep=' | ')


def lines_normalizer(array, row_num):
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


def flask_to_str(source, divider):
    div, mod = divmod(source, divider)
    return f'{mod + 1}{"↓" if div == 1 else "↑"}'


def print_split(lines, row_num, divider, header=False, stream=sys.stdout):
    splatted = [[], []]
    for group in splatted:
        for i in range(row_num):
            group.append([])

    for i, line in enumerate(lines):
        for j, el in enumerate(line):
            if j < divider:
                splatted[0][i].append(el)
            else:
                splatted[1][i].append(el)

    for cur_lines in splatted:
        for i, line in enumerate(cur_lines):
            print(*line, sep='   ' if header & (i == 0) else ' | ', file=stream)


def print_solution(start, way, stream=sys.stdout):
    curr_start = copy.deepcopy(start)
    col_num = len(curr_start)
    row_num = len(curr_start[0])
    divider = col_num // 2

    for i, step in enumerate(way):
        s, t, c = step
        print('From {} to {}. Step {} from {}'.format(
            flask_to_str(s, divider),
            flask_to_str(t, divider),
            i + 1,
            len(way)
        ), file=stream)

        header = []
        for j in range(col_num):
            cur_symbol = ' '
            if j == s:
                cur_symbol = '↑'
            if j == t:
                cur_symbol = '↓'
            header.append(cur_symbol)

        lines = lines_normalizer(curr_start, row_num)
        lines.insert(0, header)

        print_split(lines, row_num + 1, divider, header=True)

        push(curr_start, s, t)
    print("\nSolved:", file=stream)
    lines = lines_normalizer(curr_start, row_num)
    print_split(lines, row_num, divider)


class Solver:
    def __init__(self, start):
        self._initial = start

        self._col_num = len(start)
        self._row_num = len(start[0])

        self._current = self.initial
        self._way = []
        self._visited = []

    def solve(self):
        try:
            self._solve()
        except Solved:
            pass

    def _is_solved(self):
        return list(map(lambda x: len(x), self._current)).count(0) == 2

    def _is_visited(self):
        for ar in self._visited:
            if is_eq(self._current, ar):
                return True
        return False

    def _solve(self):
        self._visited.append(copy.deepcopy(self._current))
        for src, src_column in enumerate(self._current):
            for rv, rv_column in enumerate(self._current):
                if rv == src or not self.is_can_pushed(src, rv):
                    continue

                src_len = len(src_column)
                rv_len = len(rv_column)

                if if_top_equal(src_column, 1) and rv_len == 0:
                    continue
                if if_top_equal(src_column, 2) and rv_len == 0:
                    continue
                if if_top_equal(src_column, 3) and rv_len == 0:
                    continue
                if if_top_equal(src_column, 4) and rv_len == 0:
                    continue
                if if_top_equal(src_column, 2) and rv_len == 1 and src_column[-1] == rv_column[-1]:
                    continue
                if if_top_equal(src_column, 3) and rv_len > 0 and src_column[-1] == rv_column[-1]:
                    continue
                color = src_column[-1]
                push(self._current, src, rv)

                self._way.append((src, rv, color))

                if not self._is_visited():
                    if not self._is_solved():
                        self._solve()
                    else:
                        raise Solved()

                pop(self._current, src, rv)
                self._way.pop()

    def is_can_pushed(self, source, receiver):
        if len(self._current[source]) > 0 and len(self._current[receiver]) < self._row_num:
            giver = self._current[source][-1]
            if len(self._current[receiver]) == 0:
                taker = giver
            else:
                taker = self._current[receiver][-1]
            return giver == taker
        else:
            return False

    def print(self, stream=sys.stdout):
        print_solution(self.initial, self.way, stream)

    @property
    def way(self):
        return copy.deepcopy(self._way)

    @property
    def initial(self):
        return copy.deepcopy(self._initial)


if __name__ == "__main__":
    solver = Solver(start=[
        ['B', 'E', 'H', 'J', 'B'],
        ['K', 'K', 'K', 'A', 'D'],
        ['L', 'H', 'A', 'E', 'F'],
        ['A', 'B', 'C', 'H', 'L'],
        ['H', 'L', 'I', 'K', 'G'],
        ['G', 'L', 'I', 'E', 'G'],
        ['D', 'J', 'D', 'J', 'E'],
        ['I', 'J', 'G', 'C', 'D'],
        ['J', 'K', 'F', 'I', 'L'],
        ['F', 'H', 'F', 'I', 'C'],
        ['E', 'A', 'F', 'C', 'G'],
        ['A', 'B', 'B', 'C', 'D'],
        [],
        []
    ])
    solver.solve()
    solver.print()
