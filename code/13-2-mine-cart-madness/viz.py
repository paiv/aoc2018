#!/usr/bin/env python
import io
import time


def dump(track, carts, focus=None):
    with io.StringIO() as so:
        print(file=so)
        track = dict(track)
        icon = dict(zip([-1, 1, -1j, 1j], '<>^v'))
        p = None
        for k, v, _, id in carts:
            track[k] = icon[v]
            if id == focus: p = k
        ax = int(min(p.real for p in track))
        bx = int(max(p.real for p in track))
        ay = int(min(p.imag for p in track))
        by = int(max(p.imag for p in track))
        for y in range(ay, by+1):
            for x in range(ax, bx+1):
                q = (y*1j+x)
                c = track.get(q, ' ')
                if c in '<>^v':
                    print(('\033[1;37;41m' if q == p else '\033[1;37;44m'), end='', file=so)
                    # print('\033[1;37;44m', end='', file=so)
                print(c, end='', file=so)
                if c in '<>^v':
                    print('\033[0m', end='', file=so)
            print(file=so)
        print(so.getvalue())


def follow(track, carts, focus, wx=60, wy=12):
    with io.StringIO() as so:
        print(file=so)
        track = dict(track)
        icon = dict(zip([-1, 1, -1j, 1j], '<>^v'))
        p = None
        for k, v, _, id in carts:
            track[k] = icon[v]
            if id == focus: p = k
        if p is None: return
        print(f'{int(p.real)},{int(p.imag)}', file=so)
        ax = int(max(p.real - wx, min(p.real for p in track)))
        bx = int(min(ax + 2 * wx, max(p.real for p in track)))
        # ay = int(p.imag - wy)
        # by = int(p.imag + wy)
        ay = int(max(p.imag - wy, min(p.imag for p in track)))
        by = int(min(p.imag + wy, max(p.imag for p in track)))
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
        print(so.getvalue())


def viz(file, focus=0, rate=1):
    track = {(y*1j + x):v
        for y, row in enumerate(file.readlines())
        for x, v in enumerate(row)
        if not v.isspace()}

    carts = {k:v for k,v in track.items() if v in '<>^v'}

    for k, v in carts.items():
        track[k] = '-' if v in '<>' else '|'

    dirs = dict(zip('<>^v', (-1, 1, -1j, 1j)))
    carts = [(k, dirs[v], 0, i) for i, (k, v) in enumerate(carts.items())]

    dump(track, carts, focus=focus)

    turns = (-1j, 1, 1j)

    curves = {
        '\\': dict(zip([1, -1j, -1, 1j], [1j, -1, -1j, 1])),
        '/':  dict(zip([1, -1j, -1, 1j], [-1j, 1, 1j, -1])),
        }

    while len(carts) > 1:
        next_carts = list()
        hits = set(p for p, *_ in carts)
        collid = set()

        for pos, dr, turn, id in sorted(carts, key=lambda p: (p[0].imag, p[0].real)):
            hits.discard(pos)
            pos += dr

            if pos in hits:
                collid |= {id} | set(id for p,_,_,id in carts + next_carts if p == pos)
                hits.remove(pos)
            else:
                hits.add(pos)

            t = track[pos]

            if t == '+':
                dr *= turns[turn]
                turn = (turn + 1) % len(turns)
            elif t in '\\/':
                dr = curves[t][dr]

            next_carts.append((pos, dr, turn, id))

        carts = [(p,dr,h,id) for p, dr, h, id in next_carts if id not in collid]

        if focus in collid: return

        follow(track, carts, focus=focus)
        time.sleep(rate)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--focus', default=0, type=int, help='Focus on this cart')
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Track map')
    parser.add_argument('-r', '--rate', default=1/3, type=float, help='Frame rate')
    args = parser.parse_args()

    viz(file=args.file, focus=args.focus, rate=args.rate)
