#!/usr/bin/env python
import io
import itertools
import subprocess
import sys
import time
from collections import deque
from PIL import Image


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
        if hp: grid[p] = x
    dump(grid, units)


def render(board, frames, output, rate=1):
    def render_frames():
        sprites = 'elf goblin grass wall'.split()
        sims = {n:Image.open(f'sprites/{n}.png') for n in sprites}
        sprites = {k:sims[n] for n,k in zip(sprites, 'EG.#')}
        stridex, stridey = next(iter(sprites.values())).size

        ax = min(x for y,x in board.keys())
        bx = max(x for y,x in board.keys())
        ay = min(y for y,x in board.keys())
        by = max(y for y,x in board.keys())
        w,h = (bx-ax+1), (by-ay+1)

        for units in frames:
            grid = dict(board)
            for p, x, hp in units:
                if hp: grid[p] = x

            so = Image.new('RGB', (w * stridex, h * stridey))
            for y in range(ay, by+1):
                for x in range(ax, bx+1):
                    s = sprites[grid[y,x]]
                    so.paste(s, (x * stridex, y * stridey))
            yield so

    if output.endswith('.gif'):
        ims = list(render_frames())
        ims[0].save(output, save_all=True, append_images=ims[1:], duration=100, loop=True)
        for im in ims: im.close()

    elif output.endswith('.mp4'):
        ims = render_frames()
        im = next(ims)
        (w, h) = im.size

        with subprocess.Popen(f'ffmpeg -f rawvideo -s {w}x{h} -pix_fmt rgb24 -r {rate} -i - -an -codec:v mpeg4 -y {output}'.split(),
            stdin=subprocess.PIPE, stderr=subprocess.PIPE) as codec:

            codec.stdin.write(im.tobytes())
            im.close()

            for im in ims:
                try:
                    codec.stdin.write(im.tobytes())
                except BrokenPipeError:
                    print(codec.stderr.read(), file=sys.stderr)
                    break
                finally:
                    im.close()

    else:
        raise NotImplementedError()


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


def runsim(board, units, atk=3):
    frames = list()
    res = None

    for round in itertools.count():
        frames.append(list(units))

        units = sorted((p for p in units if p[2]), key=lambda p: p[0])

        for iu in range(len(units)):

            if len(set(id for _,id,hp in units if hp)) == 1:
                hp = sum(hp for _,_,hp in units)
                res = round * hp
                frames.append(list(units))
                return res, frames

            unit = units[iu]
            pos,id,hp = unit

            if not hp: continue

            goal = resolve1(unit, board, units)

            if goal:
                unit = (goal[0], id, hp)
                units[iu] = unit

            units = attack(unit, units, atk=(atk if id == 'E' else 3))


def viz(file, atk=3, rate=1, output=None):
    board = {(y, x):v for y, row in enumerate(file.readlines())
        for x, v in enumerate(row)
        if v in '#.EG'}

    state = dict(board)
    units = [(k, v, 200) for k, v in board.items() if v in 'EG']
    board = {k:('.' if v in 'EG' else v) for k, v in board.items()}

    res, frames = runsim(board, units, atk=atk)

    if output:
        render(board, frames, output, rate=rate)

    else:
        for round, units in enumerate(frames):
            trace(round)
            dump_state(board, units)
            time.sleep(1/rate)
        trace(round, 'x', res // round, '=', res)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--atk', default=3, type=int, help='Elf attack power')
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Map file')
    parser.add_argument('-r', '--rate', default=3, type=float, help='Frame rate')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()

    viz(file=args.file, atk=args.atk, rate=args.rate, output=args.output)
