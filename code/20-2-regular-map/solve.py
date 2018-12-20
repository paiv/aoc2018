#!/usr/bin/env python
from collections import deque


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
    rooms = list()
    while fringe:
        pos, path = fringe.popleft()

        if pos in visited: continue
        visited.add(pos)

        if len(path) >= 1000:
            rooms.append(pos)

        for dr, n in rmoves.items():
            tpos = pos + dr
            if grid.get(tpos, '#') in '-|':
                fringe.append((tpos + dr, path + n))

    res = len(rooms)
    return res


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
