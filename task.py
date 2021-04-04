import copy


class Solved(Exception):
    pass


class Skip(Exception):
    pass


def push(arr, source, receiver):
    arr[receiver].append(arr[source].pop(-1))


def pop(arr, source, receiver):
    arr[source].append(arr[receiver].pop(-1))


def is_solved():
    return list(map(lambda x: len(x), array)).count(0) == 2


def if_eq_column(column, n):
    return len(column) >= n and column[-n:].count(column[-1]) == n


def is_eq(ar1, ar2):
    if len(ar1) != len(ar2):
        return False
    for el1, el2 in zip(ar1, ar2):
        if el1 != el2:
            return False
    return True


def is_visited():
    for ar in visited:
        if is_eq(array, ar):
            return True
    return False


def is_can_pushed(source, receiver):
    if len(array[source]) > 0 and len(array[receiver]) < 4:
        giver = array[source][-1]
        if len(array[receiver]) == 0:
            taker = giver
        else:
            taker = array[receiver][-1]
        return giver == taker
    else:
        return False


def if_top_equal(column, n):
    return len(column) == n and column[-n:].count(column[-1]) == n and column[-1]


def solve():
    visited.append(copy.deepcopy(array))
    for src in range(count):
        for rv in range(count):
            if rv == src or not is_can_pushed(src, rv):
                continue

            src_clmn = array[src]
            rv_clmn = array[rv]

            src_len = len(src_clmn)
            rv_len = len(rv_clmn)

            if if_top_equal(src_clmn, 1) and rv_len == 0:
                continue
            if if_top_equal(src_clmn, 2) and rv_len == 0:
                continue
            if if_top_equal(src_clmn, 3) and rv_len == 0:
                continue
            if if_top_equal(src_clmn, 4) and rv_len == 0:
                continue
            if if_top_equal(src_clmn, 2) and rv_len == 1 and src_clmn[-1] == rv_clmn[-1]:
                continue
            if if_top_equal(src_clmn, 3) and rv_len > 0 and src_clmn[-1] == rv_clmn[-1]:
                continue

            color = src_clmn[-1]
            push(array, src, rv)
            way.append((src, rv, color))

            if not is_visited():
                if not is_solved():
                    solve()
                else:
                    raise Solved()

            pop(array, src, rv)
            way.pop()


def printer(array):
    line1 = []
    line2 = []
    line3 = []
    line4 = []
    for column in array:
        if len(column) == 4:
            line1.append(column[3])
            line2.append(column[2])
            line3.append(column[1])
            line4.append(column[0])
        if len(column) == 3:
            line1.append(' ')
            line2.append(column[2])
            line3.append(column[1])
            line4.append(column[0])
        if len(column) == 2:
            line1.append(' ')
            line2.append(' ')
            line3.append(column[1])
            line4.append(column[0])
        if len(column) == 1:
            line1.append(' ')
            line2.append(' ')
            line3.append(' ')
            line4.append(column[0])
        if len(column) == 0:
            line1.append(' ')
            line2.append(' ')
            line3.append(' ')
            line4.append(' ')
    print(*line1, sep=' | ')
    print(*line2, sep=' | ')
    print(*line3, sep=' | ')
    print(*line4, sep=' | ')


def find_way(start):
    global way, visited, count, array

    way = []
    visited = []
    count = len(start)
    array = copy.deepcopy(start)

    try:
        solve()
    except Solved:
        return way
    return []


def print_solution(start, way):
    curr_start = copy.deepcopy(start)
    for i, step in enumerate(way):
        src, rv, moved = step
        print(f"Step {i + 1}: move {moved} from {src + 1} to {rv + 1}")
        print(*list('↑' if src == x else '↓' if rv == x else ' ' for x in range(len(curr_start))), sep='   ')
        printer(curr_start)
        push(curr_start, src, rv)
    print("\nSolved:")
    printer(curr_start)


if __name__ == "__main__":
    start = [
        ['Y', 'B', 'R', 'B'],
        ['B', 'Y', 'R', 'R'],
        ['R', 'B', 'Y', 'Y'],
        [],
        [],
    ]

    way = find_way(start)
    print_solution(start, way)
