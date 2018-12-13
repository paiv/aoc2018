#!/usr/bin/env python
import io
import sys
import time


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def dump(track, carts):
    with io.StringIO as so:
        print(file=so)
        track = dict(track)
        icon = dict(zip([-1, 1, -1j, 1j], '<>^v'))
        for k, v, *_ in carts:
            track[k] = icon[v]
        ax = int(min(p.real for p in track))
        bx = int(max(p.real for p in track))
        ay = int(min(p.imag for p in track))
        by = int(max(p.imag for p in track))
        for y in range(ay, by+1):
            for x in range(ax, bx+1):
                c = track.get((y*1j+x), ' ')
                if c in '<>^v':
                    print('\033[1;37;44m', end='', file=so)
                print(c, end='', file=so)
                if c in '<>^v':
                    print('\033[0m', end='', file=so)
            print(file=so)
        trace(so.getvalue())


def follow(track, carts, n, wx=60, wy=16):
    with io.StringIO() as so:
        print(file=so)
        track = dict(track)
        icon = dict(zip([-1, 1, -1j, 1j], '<>^v'))
        p = None
        for k, v, _, id in carts:
            track[k] = icon[v]
            if id == n: p = k
        if p is None: return
        ax = int(max(p.real - wx, min(p.real for p in track)))
        bx = int(min(ax + 2 * wx, max(p.real for p in track)))
        ay = int(max(p.imag - wy, min(p.imag for p in track)))
        by = int(p.imag + wy)
        for y in range(ay, by+1):
            for x in range(ax, bx+1):
                q = (y*1j+x)
                c = track.get(q, ' ')
                if c in '<>^v':
                    print(('\033[1;37;41m' if q == p else '\033[1;37;44m'), end='', file=so)
                print(c, end='', file=so)
                if c in '<>^v':
                    print('\033[0m', end='', file=so)
            print(file=so)
        trace(so.getvalue())


def solve(t, focus=0):
    track = {(y*1j + x):v
        for y, row in enumerate(t.splitlines())
        for x, v in enumerate(row)
        if not v.isspace()}

    dirs = dict(zip('<>^v', (-1, 1, -1j, 1j)))

    carts = {k:v for k,v in track.items() if v in '<>^v'}

    for k, v in carts.items():
        track[k] = '-' if v in '<>' else '|'

    carts = [(k, dirs[v], 0, i) for i,(k,v) in enumerate(carts.items())]

    turns = (-1j, 1, 1j)

    curves = {
        '\\': dict(zip([1, -1j, -1, 1j], [1j, -1, -1j, 1])),
        '/':  dict(zip([1, -1j, -1, 1j], [-1j, 1, 1j, -1])),
        }

    while True:
        next_carts = list()
        hits = set(p for p,*_ in carts)

        for pos, dr, turn, id in sorted(carts, key=lambda p: (p[0].imag, p[0].real)):
            hits.remove(pos)
            pos += dr

            t = track[pos]

            if t == '+':
                dr *= turns[turn]
                turn = (turn + 1) % len(turns)

            elif t in '\\/':
                dr = curves[t][dr]

            if pos in hits:
                res = f'{int(pos.real)},{int(pos.imag)}'
                trace(res)
                return res

            next_carts.append((pos, dr, turn, id))
            hits.add(pos)

        carts = next_carts

        if 1:
            follow(track, carts, focus)
            time.sleep(0.1)


def test():
    t = r"""
|
v
|
|
|
^
|
""".strip('\n')

    assert solve(t) == '0,3'

    t = r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
""".strip('\n')

    assert solve(t) == '7,3'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
