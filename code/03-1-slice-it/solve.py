#!/usr/bin/env python
import re
import sys
from collections import defaultdict


def solve(t):
    claims = [[int(x) for x in re.findall(r'\d+', s)]
        for s in t.splitlines()]

    board = defaultdict(int)

    for _, l,t, w,h in claims:
        for y in range(t, t+h):
            for x in range(l, l+w):
                board[y,x] += 1

    return sum(x > 1 for x in board.values())


def test():
    t = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""".strip('\n')

    assert solve(t) == 4, solve(t)


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
