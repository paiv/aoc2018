#!/usr/bin/env python -OO
import re
from blist import blist


def solve(t):
    n, w = map(int, re.findall(r'-?\d+', t))
    w *= 100

    res = blist([0])
    off = 0
    score = [0] * n
    for x in range(1, w + 1):
        p = (x - 1) % n

        if x % 23 == 0:
            off = (off - 7) % len(res)
            q = res.pop(off)
            score[p] += (x + q)
            off = off % len(res)
        else:
            off = (off + 2) % len(res)
            if not off: off = len(res)
            res.insert(off, x)

    return max(score)


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
