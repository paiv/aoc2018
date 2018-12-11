#!/usr/bin/env pypy3 -O
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t):
    serial = int(t)

    def cell(x, y):
        rid = x + 10
        p = (rid * y + serial) * rid
        return (p // 100) % 10 - 5

    best = None
    best_value = float('-inf')

    for y in range(300-2):
        for x in range(300-2):
            v = sum(cell(x + dx + 1, y + dy + 1) for dy in range(3) for dx in range(3))
            if v > best_value:
                best_value = v
                best = (x + 1, y + 1)

    trace(best, best_value)
    x, y = best
    return f'{x},{y}'


def test():
    assert solve('18') == '33,45'
    assert solve('42') == '21,61'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
