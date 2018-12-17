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

    sys.setrecursionlimit(2300)
    flow = set()
    settle = set()

    def fall(pos, dr=1j):
        flow.add(pos)
        grid[pos] = '|'
        tpos = pos + 1j

        if grid.get(tpos, '.') != '#' and tpos not in flow and tpos.imag <= by:
            fall(tpos)

        if grid.get(tpos, '.') not in '#~':
            return False

        lb = pos - 1
        rb = pos + 1

        lx = grid.get(lb, '.') == '#' or (lb not in flow) and fall(lb, -1)
        rx = grid.get(rb, '.') == '#' or (rb not in flow) and fall(rb, 1)

        if (dr == 1j) and (lx and rx):
            settle.add(pos)
            grid[pos] = '~'

            while lb in flow:
                settle.add(lb)
                grid[lb] = '~'
                lb -= 1

            while rb in flow:
                settle.add(rb)
                grid[rb] = '~'
                rb += 1

        return ((dr == -1 and (lx or grid.get(lb, '.') == '#')) or
            (dr == 1 and (rx or grid.get(rb, '.') == '#')))


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
