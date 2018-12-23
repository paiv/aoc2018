#!/usr/bin/env python
import re


def md(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def solve(t):
    bots = [((x,y,z),r)
        for s in t.splitlines()
        for x,y,z,r in [map(int, re.findall(r'-?\d+', s))]]

    top = max(bots, key=lambda p: p[1])

    def inrange(p):
        return md(p[0], top[0]) <= top[1]

    res = sum(inrange(p) for p in bots)
    return res


def test():
    t = r"""
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""".strip('\n')

    assert solve(t) == 7


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
