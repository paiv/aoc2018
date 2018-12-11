#!/usr/bin/env pypy3 -O
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t, w=300):
    serial = int(t)

    def cell(x, y):
        rid = (x + 1) + 10
        p = (rid * (y + 1) + serial) * rid
        return (p // 100) % 10 - 5

    sat = [[0] * (w+1) for _ in range(w+2)]

    for y in range(w):
        for x in range(w):
            sat[y][x] = cell(x=x, y=y) + sat[y][x-1] + sat[y-1][x] - sat[y-1][x-1]

    best = (float('-inf'), None)

    for x in range(w):
        for y in range(w):
            for d in range(min(w-x, w-y)):
                v = sat[y-1][x-1] + sat[y + d][x + d] - sat[y-1][x + d] - sat[y + d][x-1]
                best = max(best, (v, (x, y, d)))

    res = ','.join(str(x+1) for x in best[1])
    trace(res)
    return res


def test():
    assert solve('18', w=5) == '1,3,3'
    assert solve('42', w=5) == '1,1,3'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
