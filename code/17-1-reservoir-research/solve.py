#!/usr/bin/env python -O
import re
import sys


def solve(t):
    grid = dict()

    for s in t.splitlines():
        xs = [*map(int, re.findall(r'-?\d+', s))]
        x = xs[0]
        for y in range(xs[1], xs[2] + 1):
            p = (x + y * 1j) if s[0] == 'x' else (y + x * 1j)
            grid[p] = '#'

    ax = int(min(p.real for p in grid))
    bx = int(max(p.real for p in grid))
    ay = int(min(p.imag for p in grid))
    by = int(max(p.imag for p in grid))

    sys.setrecursionlimit(4000)

    def spread(pos, dr):
        while grid.get(pos, '.') in '.|':
            if grid.get(pos + 1j, '.') not in '#~':
                fall(pos)
                break
            grid[pos] = '|'
            pos += dr
        return pos

    def fall(pos):
        if pos.imag > by: return
        if grid.get(pos, '.') != '.': return
        grid[pos] = '|'

        if grid.get(pos + 1j, '.') == '.':
            fall(pos + 1j)
        else:
            lb = spread(pos, -1)
            rb = spread(pos, 1)
            if grid.get(lb) == '#' == grid.get(rb):
                for x in range(int(lb.real) + 1, int(rb.real)):
                    grid[x + pos.imag * 1j] = '~'
                grid[pos - 1j] = '.'
                fall(pos - 1j)

    fall(500)
    grid[500] = '+'

    res = sum(v in '~|' for k,v in grid.items() if k.imag >= ay)
    return res


def test():
    t = r"""
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".strip('\n')

    assert solve(t) == 57


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
