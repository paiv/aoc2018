#!/usr/bin/env python
import io
import re
import sys


def dump(board):
    theme = {
        '+': '\033[1;32m+\033[0m',
        '#': '\033[2;31m#\033[0m',
        '.': '\033[2;33m.\033[0m',
        '|': '\033[1;34m|\033[0m',
        '~': '\033[1;34m~\033[0m',
    }
    with io.StringIO() as so:
        print(file=so)
        ax = int(min(p.real for p in board))
        bx = int(max(p.real for p in board))
        ay = int(min(p.imag for p in board))
        by = int(max(p.imag for p in board))
        for y in range(ay, by+1):
            for x in range(ax, bx+1):
                q = (y*1j+x)
                c = board.get(q, '.')
                print(theme[c], end='', file=so)
            print(file=so)
        print(so.getvalue())


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
    dump(grid)

    res1 = sum(v in '~|' for k,v in grid.items() if k.imag >= ay)
    res2 = sum(v in '~' for k,v in grid.items() if k.imag >= ay)
    return res1, res2


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
