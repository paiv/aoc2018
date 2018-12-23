#!/usr/bin/env pypy3 -OO
import math
import re
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def md(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def inrange(bot, p):
    return md(bot[0], p) <= bot[1]


def minmax(xs):
    g = iter(xs)
    n = m = next(g)
    for x in g:
        n = min(n, x)
        m = max(m, x)
    return (n, m)


def intersect(a, b):
    (ax, ay), (bx, by) = a, b
    return ax <= by <= ay or bx <= ay <= by


def solve(t):
    bots = [((x,y,z),r)
        for s in t.splitlines()
        for x,y,z,r in [map(int, re.findall(r'-?\d+', s))]]

    ax, bx = minmax(x for (x,y,z),r in bots)
    ay, by = minmax(y for (x,y,z),r in bots)
    az, bz = minmax(z for (x,y,z),r in bots)

    step = 2 ** (int(math.log2(max(bx - ax, by - ay, bz - az))) + 1)
    trace((ax, bx), (ay, by), (az, bz), 'step', step)

    best_pos = None
    best_res = float('inf')
    origin = (0,0,0)

    while step > 0:
        best_count = 0

        trace(step, '--', (ax, bx), (ay, by), (az, bz))

        for z in range(az, bz + 1, step):
            for y in range(ay, by + 1, step):
                for x in range(ax, bx + 1, step):
                    pos = (x, y, z)
                    counts = 0
                    dist = md(origin, pos)

                    for bot in bots:
                        bot_pos, bot_r = bot
                        counts += md(pos, bot_pos) < bot_r + step

                    if (counts > best_count) or (counts == best_count and dist < best_res):
                        # print('**', pos, f'({counts})', dist)
                        best_count = counts
                        best_pos = pos
                        best_res = dist

        x, y, z = best_pos
        ax, bx = x - 2 * step, x + 2 * step
        ay, by = y - 2 * step, y + 2 * step
        az, bz = z - 2 * step, z + 2 * step
        step //= 2

        trace('best:', f'({best_count})', 'at', best_pos, '=', best_res)

    return best_res


def test():
    t = r"""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""".strip('\n')

    assert solve(t) == 36


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
