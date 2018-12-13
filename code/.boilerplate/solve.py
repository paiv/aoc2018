#!/usr/bin/env python
import re
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t):
    t = [[*map(int, re.findall(r'-?\d+', s))]
        for s in t.splitlines()]
    pass


def test():
    t = r"""
""".strip('\n')

    # assert solve(t) == 0

    # assert solve('') == 0


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
