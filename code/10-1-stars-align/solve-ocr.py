#!/usr/bin/env python -O
import itertools
import operator
import re
import sys
from functools import reduce


VERBOSE = 2 if __debug__ else 0

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


class Ocr:
    tables = [
"""
A       B       C       E       F       G       H       J       K       L       N       P       R       X       Z
..##....#####....####...######..######...####...#....#.....###..#....#..#.......#....#..#####...#####...#....#..######..
.#..#...#....#..#....#..#.......#.......#....#..#....#......#...#...#...#.......##...#..#....#..#....#..#....#.......#..
#....#..#....#..#.......#.......#.......#.......#....#......#...#..#....#.......##...#..#....#..#....#...#..#........#..
#....#..#....#..#.......#.......#.......#.......#....#......#...#.#.....#.......#.#..#..#....#..#....#...#..#.......#...
#....#..#####...#.......#####...#####...#.......######......#...##......#.......#.#..#..#####...#####.....##.......#....
######..#....#..#.......#.......#.......#..###..#....#......#...##......#.......#..#.#..#.......#..#......##......#.....
#....#..#....#..#.......#.......#.......#....#..#....#......#...#.#.....#.......#..#.#..#.......#...#....#..#....#......
#....#..#....#..#.......#.......#.......#....#..#....#..#...#...#..#....#.......#...##..#.......#...#....#..#...#.......
#....#..#....#..#....#..#.......#.......#...##..#....#..#...#...#...#...#.......#...##..#.......#....#..#....#..#.......
#....#..#####....####...######..#........###.#..#....#...###....#....#..######..#....#..#.......#....#..#....#..######..
"""
]

    def __init__(self):
        table = list()
        abc = list()
        height = None
        for t in self.tables:
            h, *_ = t.strip('\n').splitlines()
            abc.extend(h.split())
            table.extend(Ocr._split(t))
            height = len(table[-1])
        self.table = {abc[i]:char for i, char in enumerate(table)}
        self.rtable = {char:abc[i] for i, char in enumerate(table)}
        self.height = height

    def _split(text):
        t = re.sub(r'[^#.\n]', ' ', text).strip()
        xs = [[x == '#' for x in row] for row in t.splitlines()]
        for k, g in itertools.groupby(zip(*xs), any):
            if k: yield tuple(zip(*g))

    def scan(self, text):
        return ''.join(self.rtable.get(x, '?') for x in Ocr._split(text))

    def print(self, text, char_space=2):
        xs = (self.table[x] for x in text if x in self.table)
        sp = tuple((False,)*char_space for _ in range(self.height))
        xs = (x for p in xs for x in [p, sp])
        return Ocr._render([reduce(operator.add, row) for row in zip(*xs)])

    def _render(char):
        return '\n'.join(''.join('#' if x else '.' for x in row) for row in char)


def display(points, t=0):
    xs = [(x + dx * t) for x,_,dx,_ in points]
    ys = [(y + dy * t) for _,y,_,dy in points]
    ax,bx = min(xs), max(xs)
    ay,by = min(ys), max(ys)
    grid = set(zip(xs, ys))

    return '\n'.join(''.join('#' if (x,y) in grid else '.'
        for x in range(ax, bx + 1))
        for y in range(ay, by + 1))


def solve(t):
    points = [[*map(int, re.findall(r'-?\d+', s))]
        for s in t.splitlines()]

    ocr = Ocr()
    mindy = float('inf')

    for t in range(10000000):
        ys = [(y + dy * t) for _,y,_,dy in points]
        dy = max(ys) - min(ys)
        if dy > mindy:
            trace(t-1, dy)
            break
        else:
            mindy = dy

    res = ocr.scan(display(points, t-1))
    trace(ocr.print(res))
    return res


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
