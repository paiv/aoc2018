#!/usr/bin/env python
import io
from collections import deque


def dump(grid, unk='?'):
    theme = {
        'X': '\033[1;32mX\033[0m',
        '#': '\033[2;33m#\033[0m',
        '.': '\033[2;33m.\033[0m',
        '|': '\033[0;37m|\033[0m',
        '-': '\033[0;37m-\033[0m',
        '?': '\033[0;31m?\033[0m',
    }
    with io.StringIO() as so:
        print(file=so)
        ax = int(min(p.real for p in grid))
        bx = int(max(p.real for p in grid))
        ay = int(min(p.imag for p in grid))
        by = int(max(p.imag for p in grid))
        for y in range(ay, by+1):
            for x in range(ax, bx+1):
                q = (y*1j+x)
                c = grid.get(q, unk)
                print(theme[c], end='', file=so)
            print(file=so)
        print(so.getvalue())


def solve(t):
    moves = dict(E=1, N=-1j, W=-1, S=1j)
    rmoves = {v:k for k,v in moves.items()}

    grid = dict()
    start = 0
    rx = iter(t)

    def branch(start):
        pos = start

        for c in rx:
            if c in 'ENWS':
                dr = moves[c]
                grid[pos + dr] = '-|'[abs(int(dr.real))]
                grid[pos + dr + dr*1j] = '#'
                grid[pos + dr + dr*-1j] = '#'
                pos += 2*dr
                grid[pos] = '.'
                grid[pos + dr + dr*1j] = '#'
                grid[pos + dr + dr*-1j] = '#'

            elif c == '(':
                branch(pos)

            elif c == ')':
                return

            elif c == '|':
                pos = start

            elif c == '$':
                break

            elif c == '^':
                grid[start] = 'X'

    branch(start)

    fringe = deque([(start, '')])
    visited = set()
    while fringe:
        pos, path = fringe.popleft()

        if pos in visited: continue
        visited.add(pos)

        for dr, n in rmoves.items():
            tpos = pos + dr
            if grid.get(tpos, '#') in '-|':
                fringe.append((tpos + dr, path + n))

    return grid


def viz(file):
    grid = solve(file.read())
    dump(grid, unk='#')


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Regex input')
    args = parser.parse_args()

    viz(file=args.file)
