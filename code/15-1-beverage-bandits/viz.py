#!/usr/bin/env pypy3
import io
import itertools
import sys
import time
from collections import deque


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def dump(board, units=None):
    with io.StringIO() as so:
        def dgr(s): return f'\033[2;37m{s}\033[0m'
        theme = {
            '#': '\033[2;37m#\033[0m',
            '.': '\033[2;32m.\033[0m',
            'E': '\033[1;33mE\033[0m',
            'G': '\033[32mG\033[0m',
            '?': '\033[1;37mG\033[0m',
            '*': '\033[1;37mG\033[0m',
        }
        bx = max(x for (y, x) in board.keys())
        by = max(y for (y, x) in board.keys())
        for y in range(by+1):
            with io.StringIO() as line:
                for x in range(bx+1):
                    c = board[(y,x)]
                    print(theme.get(c, c), end='', file=line)
                us = sorted((px,id,hp) for (py,px),id,hp in (units or []) if py == y and hp)
                us = dgr(', ').join(f"{theme[id]}{dgr('(')}{hp}{dgr(')')}" for _,id,hp in us)
                print('  ', us, end='', file=line)
                print(line.getvalue(), file=so)
        trace(so.getvalue())


def dump_state(board, units):
    if VERBOSE < 2: return
    grid = dict(board)
    for p, x, hp in units:
        if hp:
            grid[p] = x
    dump(grid, units)


def goal(unit, targets, board):
    fringe = deque()
    visited = set()

    start = unit[0]
    fringe.append((start, tuple()))

    while fringe:
        pos, path = fringe.popleft()
        (py,px) = pos

        if pos in targets:
            return path
        if pos in visited: continue
        visited.add(pos)

        for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]:
            tpos = (py+dy, px+dx)
            if board.get(tpos, None) == '.':
                fringe.append((tpos, path + (tpos,)))


def resolve1(unit, board, units):
    grid = dict(board)
    for p, x, hp in units:
        if hp: grid[p] = x

    pos,id,hp = unit

    ts = set(tpos
        for (y,x),tid,thp in units
        if tid != id and thp
        for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]
        for tpos in [(y+dy,x+dx)]
        if grid.get(tpos, None) == '.' or tpos == pos)

    if pos in ts: return []

    return goal(unit, ts, grid)


def attack(unit, units, atk=3):
    pos, id, hp = unit
    y,x = pos

    moves = [(-1,0),(0,-1),(0,1),(1,0)]
    ts = [(y+dy, x+dx) for dy,dx in moves]

    targets = [(thp, t, i) for i,t in enumerate(units)
        for tpos,tid,thp in [t]
        if tid != id and tpos in ts and thp]

    if targets:
        _,(tpos,tid,thp),i = sorted(targets)[0]
        thp = max(0, thp - atk)
        units2 = list(units)
        units2[i] = (tpos,tid,thp)
        return units2

    return units


def viz(file, atk=3, rate=1):
    board = {(y, x):v for y, row in enumerate(file.readlines())
        for x, v in enumerate(row)
        if v in '#.EG'}

    state = dict(board)
    units = [(k, v, 200) for k, v in board.items() if v in 'EG']
    board = {k:('.' if v in 'EG' else v) for k, v in board.items()}

    for round in itertools.count():
        if 1:
            trace(round)
            dump_state(board, units)
            time.sleep(rate)

        units = sorted((p for p in units if p[2]), key=lambda p: p[0])

        for iu in range(len(units)):

            if len(set(id for _,id,hp in units if hp)) == 1:
                if 1:
                    trace(round)
                    dump_state(board, units)
                hp = sum(hp for _,_,hp in units)
                trace(round, 'x', hp, '=', round * hp)
                return round * hp

            unit = units[iu]
            pos,id,hp = unit

            if not hp: continue

            goal = resolve1(unit, board, units)

            if goal:
                unit = (goal[0], id, hp)
                units[iu] = unit

            units = attack(unit, units, atk=(atk if id == 'E' else 3))


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--atk', default=3, type=int, help='Elf attack power')
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Map file')
    parser.add_argument('-r', '--rate', default=1/3, type=float, help='Frame rate')
    args = parser.parse_args()

    viz(file=args.file, atk=args.atk, rate=args.rate)
