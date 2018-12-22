#!/usr/bin/env python
import re


def solve(t):
    depth, w, h = [*map(int, re.findall(r'-?\d+', t))]
    w += 1
    h += 1

    erosion = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if (x,y) in ((0,0), (w-1, h-1)):
                continue
            if y == 0:
                erosion[y][x] = (x * 16807 + depth) % 20183
            elif x == 0:
                erosion[y][x] = (y * 48271 + depth) % 20183
            else:
                erosion[y][x] = (erosion[y][x-1] * erosion[y-1][x] + depth) % 20183

    grid = [[(x % 3) for x in row] for row in erosion]

    res = sum(x for row in grid for x in row)
    return res


def test():
    t = r"""
depth: 510
target: 10,10
""".strip('\n')

    assert solve(t) == 114


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
