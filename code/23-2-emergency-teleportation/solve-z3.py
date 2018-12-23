#!/usr/bin/env python -OO
import z3
import re
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def md(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def solve(t):
    bots = [((x,y,z),r)
        for s in t.splitlines()
        for x,y,z,r in [map(int, re.findall(r'-?\d+', s))]]

    def z3abs(x):
        return z3.If(x < 0, -x, x)

    def z3md(a, b):
        ax, ay, az = a
        bx, by, bz = b
        return z3abs(bx - ax) + z3abs(by - ay) + z3abs(bz - az)

    model = z3.Optimize()
    bot_count, X, Y, Z = z3.Ints('BotCount X Y Z')
    goal = (X, Y, Z)
    bot_count *= 0
    origin = (0,0,0)

    for p, r in bots:
        t = z3md(goal, p) <= r
        bot_count += z3.If(t, 1, 0)

    model.maximize(bot_count)
    model.minimize(z3md(origin, goal))
    trace(model)

    model.check()
    m = model.model()
    trace(m)

    res = md(origin, [m[i].as_long() for i in goal])

    trace(res)
    return res


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
