#!/usr/bin/env pypy3 -O
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t, w=300):
    serial = int(t)

    def cell(x, y):
        rid = x + 10
        p = (rid * y + serial) * rid
        return (p // 100) % 10 - 5

    cells = [[cell(x, y) for x in range(1, w+1)] for y in range(1, w+1)]

    if 0:
        for row in cells:
            for v in row:
                trace(f'{v:2}', end=' ')
            trace()

    best = None
    best_value = float('-inf')

    for y in range(w):
        for x in range(w):
            v = 0
            for d in range(min(w-x, w-y)):
                v += sum(cells[y+d][qx] for qx in range(x, x+d+1)) + sum(cells[qy][x+d] for qy in range(y, y+d))
                if v > best_value:
                    best_value = v
                    best = (x + 1, y + 1, d + 1)
                    trace(best, best_value)

    trace(best, best_value)
    return ','.join(map(str, best))


def test():
    assert solve('18', w=5) == '1,3,3'
    assert solve('42', w=5) == '1,1,3'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
