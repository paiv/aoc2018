#!/usr/bin/env python -OO
import re
from collections import defaultdict


def solve(t, max_dist=10000):
    points = [tuple(map(int, re.findall(r'-?\d+', s)))
        for s in t.splitlines()]

    xa = min(x for x,_ in points)
    xb = max(x for x,_ in points)
    ya = min(y for _,y in points)
    yb = max(y for _,y in points)

    def md(a, b):
        (xa, ya), (xb, yb) = a, b
        return abs(xb - xa) + abs(yb - ya)

    res = 0
    for y in range(ya, yb + 1):
        for x in range(xa, xb + 1):
            d = sum(md((x,y), p) for p in points)
            if d < max_dist:
                res += 1
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

    assert solve(t, 32) == 16


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
