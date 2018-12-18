#!/usr/bin/env python
import io
import subprocess
import sys
import time
from PIL import Image


def dump(grid, w, h):
    theme = {
        '#': '\033[0;31m#\033[0m',
        '.': '\033[0;32m.\033[0m',
        '|': '\033[1;32m|\033[0m',
    }
    with io.StringIO() as so:
        print(file=so)
        for y in range(h):
            for x in range(w):
                q = (y*1j+x)
                c = grid.get(q, '.')
                print(theme[c], end='', file=so)
            print(file=so)
        print(so.getvalue())


def render(size, frames, output, rate=1):
    def render_frames():
        sprites = 'grass trees lumber'.split()
        sims = {n:Image.open(f'sprites/{n}.png') for n in sprites}
        sprites = {k:sims[n] for n,k in zip(sprites, '.|#')}
        stridex, stridey = next(iter(sprites.values())).size
        w, h = size

        for grid in frames:
            so = Image.new('RGB', (w * stridex, h * stridey))
            for y in range(h):
                for x in range(w):
                    s = sprites[grid.get(x+y*1j, '.')]
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

        # out_fmt = '-codec:v mpeg4'
        out_fmt = '-codec:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -preset veryslow'
        ffmpeg = f'ffmpeg -f rawvideo -s {w}x{h} -pix_fmt rgb24 -r {rate} -i - -an {out_fmt} -y {output}'.split()

        with subprocess.Popen(ffmpeg, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as codec:

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


def solve(grid, w, h):
    rounds = [grid]

    for t in range(1, 1000000000):
        next_grid = dict()
        for y in range(h):
            for x in range(w):
                pos = x + y*1j
                c = grid.get(pos, '.')

                ya = te = 0
                for a in (-1, 0, 1):
                    for b in (-1j, 0, 1j):
                        d = a + b
                        if d:
                            q = grid.get(pos + d, '.')
                            te += q == '|'
                            ya += q == '#'

                if c == '.':
                    if te >= 3:
                        next_grid[pos] = '|'
                elif c == '|':
                    next_grid[pos] = '#' if ya >= 3 else '|'
                elif c == '#':
                    if (ya > 0 < te):
                        next_grid[pos] = '#'

        grid = next_grid

        if grid in rounds: break
        rounds.append(grid)

    a, = [i for i, x in enumerate(rounds) if x == grid]

    grid = rounds[a + (1000000000 - a) % (t - a)]

    ts = sum(x == '|' for x in grid.values())
    ns = sum(x == '#' for x in grid.values())
    res = ts * ns
    return res, rounds


def viz(file, rate=1, output=None):
    grid = {(x + y * 1j):v
        for y, row in enumerate(file.readlines())
        for x, v in enumerate(row)
        if v in '.#|'}
    w = int(max(p.real for p in grid)) + 1
    h = int(max(p.imag for p in grid)) + 1

    res, frames = solve(grid, w=w, h=h)

    if output:
        render((w, h), frames, output, rate=rate)
    else:
        for round, state in enumerate(frames):
            print(round)
            dump(state, w=w, h=h)
            time.sleep(1/rate)
        print(res)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Map file')
    parser.add_argument('-r', '--rate', default=10, type=float, help='Frame rate')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()

    viz(file=args.file, rate=args.rate, output=args.output)
