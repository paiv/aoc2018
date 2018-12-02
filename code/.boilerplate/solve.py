#!/usr/bin/env python
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t):
    t = t.splitlines()
    pass


def test():
    t = """
""".strip('\n')

    # assert solve(t) == 0, solve(t)

    # assert solve('') == 0


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
