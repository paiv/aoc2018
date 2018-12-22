#!/usr/bin/env python
import io
import itertools
import heapq
import re
import subprocess
import time
from functools import lru_cache
from PIL import Image


def dump(grid, target, path):
    theme = {
        ' ': '\033[30m \033[0m',
        '.': '\033[37m.\033[0m',
        '=': '\033[34m=\033[0m',
        '|': '\033[37m|\033[0m',
        '-': '\033[30;43m-\033[0m',
        '^': '\033[30;43m^\033[0m',
        '*': '\033[30;43m*\033[0m',
        'X': '\033[31mX\033[0m',
    }

    bx = int(max(p.real for p in grid))
    by = int(max(p.imag for p in grid))
    path = {p: '-^*'[t] for p,t in path}

    with io.StringIO() as so:
        print(file=so)
        for y in range(by+1):
            for x in range(bx+1):
                p = x + y*1j

                if p in path:
                    c = path[p]
                    print(theme[c], end='', file=so)
                elif p == target:
                    print(theme['X'], end='', file=so)
                else:
                    c = grid.get(p, ' ')
                    print(theme[c], end='', file=so)

            print(file=so)
        print(so.getvalue(), end='')


def render(text, output, window=80, rate=1, speed=1):
    def render(frame):
        grid, target, path = frame

        sprites = 'blank gear goal narrow notool rock space torch water'.split()
        symbols = '?^X|-. *='
        sims = {n:Image.open(f'sprites/{n}.png') for n in sprites}
        sprites = {k:sims[n] for n,k in zip(sprites, symbols)}
        stridex, stridey = next(iter(sprites.values())).size

        for bg,tt,sp in itertools.product(' X', ' -^*', '?.=|'):
            key = bg+tt+sp
            bim = sprites[bg].convert('RGBA')
            tim = sprites[tt].convert('RGBA')
            sim = sprites[sp].convert('RGBA')
            s = Image.alpha_composite(bim, tim)
            s.alpha_composite(sim)
            sprites[key] = s

        ax = int(min(p.real for p in grid))
        ay = int(min(p.imag for p in grid))
        bx = int(max(p.real for p in grid))
        by = int(max(p.imag for p in grid))
        w, h = (bx - ax + 1), (by - ay + 1)
        path = {p: '-^*'[t] for p,t in path}

        so = Image.new('RGBA', (w * stridex, h * stridey))

        for y in range(ay, by+1):
            for x in range(ax, bx+1):
                p = x + y*1j
                k = '{} {}'.format('X' if p == target else ' ', grid.get(p, '?'))
                s = sprites[k]
                so.paste(s, (x * stridex, y * stridey))

        for p, t in path.items():
            k = '{}{}{}'.format('X' if p == target else ' ', t, '?' if p == target else grid.get(p, ' '))
            s = sprites[k]
            x, y = map(int, (p.real, p.imag))
            so.paste(s, (x * stridex, y * stridey))

        return so


    if output.endswith('.png'):
        frame = None
        for frame in solve(text): pass

        with render(frame) as im:
            im.save(output)

    else:
        raise NotImplementedError()


def solve(t, all_frames=False):
    depth, w, h = [*map(int, re.findall(r'-?\d+', t))]
    target = w + h * 1j

    @lru_cache(maxsize=None)
    def erosion(at):
        if (not at) or (at == target):
            return 0
        if not at.imag:
            return (int(at.real) * 16807 + depth) % 20183
        elif not at.real:
            return (int(at.imag) * 48271 + depth) % 20183
        else:
            return (erosion(at-1) * erosion(at-1j) + depth) % 20183

    def risk(at):
        return '.=|'[erosion(at) % 3]

    NEI, GEAR, TORCH = range(3)
    usable = {'.': {GEAR, TORCH}, '=': {NEI, GEAR}, '|': {NEI, TORCH}}

    def md(a, b):
        return abs(b.real - a.real) + abs(b.imag - a.imag)

    fringe = [(md(0, target), 0, [((0,0), TORCH)])]
    visited = set()
    explored = dict()

    while fringe:
        _, cost, path = heapq.heappop(fringe)
        (x,y), tool = path[-1]
        pos = x + y*1j

        explored[pos] = risk(pos)
        if all_frames:
            ipath = [(px+py*1j, t) for (px,py),t in path]
            yield (explored, target, ipath)

        if pos == target and tool == TORCH:
            if not all_frames:
                ipath = [(px+py*1j, t) for (px,py),t in path]
                yield (explored, target, ipath)
            break

        k = (pos, tool)
        if k in visited: continue
        visited.add(k)

        for tt in ({NEI, GEAR, TORCH} - {tool}):
            if tt in usable[risk(pos)]:
                heapq.heappush(fringe, (md(pos, target) + cost + 7, cost + 7, path + [((pos.real, pos.imag), tt)]))

        for dr in (1, 1j, -1j, -1):
            tpos = pos + dr
            if tpos.real < 0 or tpos.imag < 0:
                continue
            if tool in usable[risk(tpos)]:
                heapq.heappush(fringe, (md(tpos, target) + cost + 1, cost + 1, path + [((tpos.real, tpos.imag), tool)]))

    print('part2:', cost)


def viz(file, rate=1, output=None):
    text = file.read()

    if output:
        render(text, output, rate=rate)
    else:
        for frame in solve(text, all_frames=True):
            dump(*frame)
            time.sleep(1/rate)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Input file')
    parser.add_argument('-r', '--rate', default=20, type=float, help='Frame rate')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()

    viz(file=args.file, rate=args.rate, output=args.output)
