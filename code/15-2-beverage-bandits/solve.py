#!/usr/bin/env pypy3 -O
import itertools
import sys
from collections import deque


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


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
        return units2, (tid == 'E' and not thp)

    return units, False


def solve1(board, atk=3):
    state = dict(board)
    units = [(k, v, 200) for k, v in board.items() if v in 'EG']
    board = {k:('.' if v in 'EG' else v) for k, v in board.items()}

    for round in itertools.count():
        units = sorted((p for p in units if p[2]), key=lambda p: p[0])

        for iu in range(len(units)):

            if len(set(id for _,id,hp in units if hp)) == 1:
                hp = sum(hp for _,_,hp in units)
                trace(atk, id, round, 'x', hp, '=', round * hp)
                return id, round * hp

            unit = units[iu]
            pos,id,hp = unit

            if not hp: continue

            goal = resolve1(unit, board, units)

            if goal:
                unit = (goal[0], id, hp)
                units[iu] = unit

            units, elf_dead = attack(unit, units, atk=(atk if id == 'E' else 3))
            if elf_dead:
                return None, None


def solve(t):
    board = {(y, x):v for y, row in enumerate(t.strip().splitlines())
        for x, v in enumerate(row)}

    for atk in itertools.count(4):
        trace(atk)
        id, res = solve1(board, atk)
        if id == 'E':
            return res


def test():
    t = r"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".strip('\n')

    assert solve(t) == 4988

    t = r"""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""".strip('\n')

    assert solve(t) == 31284

    t = r"""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".strip('\n')

    assert solve(t) == 3478

    t = r"""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""".strip('\n')

    assert solve(t) == 6474

    t = r"""
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""".strip('\n')

    assert solve(t) == 1140


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
