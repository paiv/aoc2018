#!/usr/bin/env python -OO
import re
import string
import sys
from collections import defaultdict


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t):
    points = [tuple(map(int, re.findall(r'-?\d+', s)))
        for s in t.splitlines()]

    xa = min(x for x,_ in points)
    xb = max(x for x,_ in points)
    ya = min(y for _,y in points)
    yb = max(y for _,y in points)
    trace(xa, xb, ya, yb)

    trace(points)

    def md(a, b):
        (xa, ya), (xb, yb) = a, b
        return abs(xb - xa) + abs(yb - ya)

    grid = defaultdict(int)
    borders = set()
    for y in range(ya, yb + 1):
        for x in range(xa, xb + 1):
            qs = sorted((md((x,y), p), p) for p in points)
            (du, u), (dv, v) = qs[:2]
            if du != dv:
                grid[u] += 1
                if (x in (xa, xb)) or (y in (ya, yb)):
                    borders.add(u)

    trace(grid)
    trace(borders)


    if 0:
        abc = string.ascii_letters
        for y in range(ya-1, yb + 1):
            for x in range(xa-1, xb + 2):
                qs = sorted((md((x,y), p), p) for p in points)
                (du, u), (dv, v) = qs[:2]
                if du != dv:
                    if (x, y) == u:
                        cq = '*'
                    else:
                        cq = abc[points.index(u)]
                    trace(cq, end='')
                else:
                    trace('.', end='')
            trace()

    res = max(v for k,v in grid.items() if k not in borders)
    return res


def test():
    t = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip('\n')

    assert solve(t) == 17


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
