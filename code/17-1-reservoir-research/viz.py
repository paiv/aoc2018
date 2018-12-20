#!/usr/bin/env python
import io
import itertools
import subprocess
import re
import sys
import time
from PIL import Image


def dump(board, focus, window=30, windowx=30):
    theme = {
        '+': '\033[1;32m+\033[0m',
        '#': '\033[2;37m#\033[0m',
        '.': '\033[2;33m.\033[0m',
        '|': '\033[0;37m|\033[0m',
        '~': '\033[1;34m~\033[0m',
    }
    with io.StringIO() as so:
        print(file=so)
        ax = int(min(p.real for p in board))
        bx = int(max(p.real for p in board))
        ay = int(min(p.imag for p in board))
        by = int(max(p.imag for p in board))
        for y in range(max(ay, int(focus.imag) - window), min(by+1, int(focus.imag) + window)):
            for x in range(max(ax, int(focus.real) - windowx), min(bx+1, int(focus.real) + windowx)):
                q = (x + y * 1j)
                c = board.get(q, '.')
                print(theme[c], end='', file=so)
            print(file=so)
        print(so.getvalue(), end='')


def render(text, output, window=65, rate=1, speed=1):
    def render_frames():
        sprites = 'clay fall sand spring still'.split()
        sims = {n:Image.open(f'sprites/{n}.png') for n in sprites}
        sprites = {k:sims[n] for n,k in zip(sprites, '#|.+~')}
        stridex, stridey = next(iter(sprites.values())).size

        ax = ay = bx = by = w = h = so = None
        prev = dict()
        prev_focus = 500

        def xx(focus):
            top = max(0, int(focus.imag) - window)
            bottom = min(by + 1, top + window * 2)
            crop = dict()
            for y in range(top, bottom):
                for x in range(ax, bx+1):
                    crop[x-ax+(y-top)*1j] = grid.get(x+y*1j, '.')

            diff = {p:c
                for y in range(h) for x in range(w)
                for p in [x+y*1j] for c in [crop.get(p, '.')]
                if prev.get(p, '?') != c}

            for p, c in diff.items():
                x, y = int(p.real), int(p.imag)
                s = sprites[c]
                so.paste(s, (x * stridex, y * stridey))

            return crop


        for nframes, (focus, grid) in enumerate(solve(text)):
            grid[500] = '+'

            if ax is None:
                ax = int(min(p.real for p in grid))
                bx = int(max(p.real for p in grid))
                ay = int(min(p.imag for p in grid))
                by = int(max(p.imag for p in grid))
                w, h = (bx - ax + 1), (by - ay + 1)
                h = min(window * 2, h)

                so = Image.new('RGB', (w * stridex, h * stridey))

            if nframes % speed != 0:
                continue

            if 0 > focus.imag - prev_focus.imag > -(window * 0.8):
                focus = prev_focus

            crop = xx(focus)

            yield so
            prev = crop
            prev_focus = focus

        else:
            if nframes % speed != 0:
                crop = xx(focus)
                yield so


    if output.endswith('.gif'):
        ims = list(render_frames())
        ims[0].save(output, save_all=True, append_images=ims[1:], duration=100, loop=True)
        for im in ims: im.close()

    elif output.endswith('.mp4'):
        ims = render_frames()
        im = next(ims)
        (w, h) = im.size

        # out_fmt = '-codec:v mpeg4'
        out_fmt = '-codec:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -preset veryslow'
        if (w % 2) or (h % 2):
             out_fmt += ' -vf scale=trunc(iw/2)*2:trunc(ih/2)*2'
        ffmpeg = f'ffmpeg -f rawvideo -s {w}x{h} -pix_fmt rgb24 -r {rate} -i - -an {out_fmt} -y {output}'.split()

        with subprocess.Popen(ffmpeg, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL) as codec:

            codec.stdin.write(im.tobytes())
            # im.close()

            for im in ims:
                try:
                    data = im.tobytes()
                    codec.stdin.write(data)

                    print('.', end='', flush=True)
                except BrokenPipeError:
                    print('!', file=sys.stderr)
                    _, err = codec.communicate()
                    print(err, file=sys.stderr)
                    break
                finally:
                    # im.close()
                    pass
            else:
                print()

    else:
        raise NotImplementedError()


def solve(text):
    grid = dict()

    for s in text.splitlines():
        xs = [*map(int, re.findall(r'-?\d+', s))]
        x = xs[0]
        for y in range(xs[1], xs[2] + 1):
            p = (x + y * 1j) if s[0] == 'x' else (y + x * 1j)
            grid[p] = '#'

    ax = int(min(p.real for p in grid))
    bx = int(max(p.real for p in grid))
    ay = int(min(p.imag for p in grid))
    by = int(max(p.imag for p in grid))
    grid[500] = '+'

    def resolve_stills(pos):
        lb = rb = pos
        while grid.get(lb, '.') != '#' and grid.get(lb + 1j, '.') in '#~':
            lb -= 1
        while grid.get(rb, '.') != '#' and grid.get(rb + 1j, '.') in '#~':
            rb += 1
        s = grid.get(lb, '.') == '#' == grid.get(rb, '.')
        return s


    leaks = [(500, 1j)]
    yield (500, dict(grid))

    while leaks:
        fringe = leaks
        leaks = set()
        focus = 0
        prev = dict(grid)

        for pos, dr in fringe:
            tpos = pos + dr
            if tpos.imag > by:
                continue
            c = prev.get(pos, '.')
            cc = grid.get(pos, '.')
            q = prev.get(tpos, '.')

            if c in '|+' and dr == 1j:
                if q == '.':
                    grid[tpos] = '|'
                    leaks.add((tpos, dr))
                    focus = max(focus, tpos.imag)
                elif q in '#~':
                    leaks.add((pos, dr*1j))
                    leaks.add((pos, dr*-1j))
                    focus = max(focus, pos.imag)

            elif c in '|' and dr in (-1, 1):
                z = prev.get(tpos + 1j, '.')
                if q == '.' and z in '#~':
                    grid[tpos] = '|'
                    leaks.add((tpos, dr))
                    focus = max(focus, tpos.imag)
                elif q == '.' and z == '.':
                    grid[tpos] = '|'
                    leaks.add((tpos, 1j))
                    focus = max(focus, tpos.imag)
                else:
                    if resolve_stills(pos):
                        grid[pos] = '~'
                        leaks.add((pos, dr))
                        leaks.add((pos, dr*-1))
                        focus = max(focus, pos.imag)

            elif c in '~' and dr in (-1, 1):
                focus = max(focus, tpos.imag)
                if q == '|':
                    grid[tpos] = '~'
                    leaks.add((tpos, dr))
                elif q in '.':
                    grid[tpos] = '|'
                    leaks.add((tpos, dr))
                elif q in '~#':
                    lb = rb = pos
                    ws = set()
                    while prev.get(lb, '.') == '~':
                        ws.add(lb)
                        lb -= 1
                    while prev.get(rb, '.') == '~':
                        ws.add(rb)
                        rb += 1
                    if prev.get(lb) == '#' == prev.get(rb):
                        for tpos in ws:
                            if prev.get(tpos - 1j, '.') == '|':
                                leaks.add((tpos - 1j, -1))
                                leaks.add((tpos - 1j, 1))

        yield (500+focus*1j, dict(grid))

    # dump(grid, 500, window=100000, windowx=100000)
    res1 = sum(v in '~|' for k,v in grid.items() if k.imag >= ay)
    res2 = sum(v in '~' for k,v in grid.items() if k.imag >= ay)
    print()
    print('part1:', res1)
    print('part2:', res2)


def viz(file, rate=1, speed=1, output=None, quiet=False):
    text = file.read()

    if output:
        render(text, output, rate=rate, speed=speed)
    else:
        for focus, frame in itertools.islice(solve(text), None, None, speed):
            if not quiet:
                dump(frame, focus)
                time.sleep(1/rate)
        else:
            if quiet:
                dump(frame, focus)


def handle_sigusr1(sig, frame):
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    import argparse
    import signal
    import sys

    signal.signal(signal.SIGUSR1, handle_sigusr1)

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Map file')
    parser.add_argument('-r', '--rate', default=60, type=float, help='Frame rate')
    parser.add_argument('-s', '--speed', default=1, type=int, help='Playback speed')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-q', '--quiet', action='store_true', help='Render final state only')
    args = parser.parse_args()

    viz(file=args.file, rate=args.rate, speed=args.speed, output=args.output, quiet=args.quiet)
