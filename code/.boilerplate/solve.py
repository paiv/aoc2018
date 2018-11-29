#!/usr/bin/env python
import sys


VERBOSE = 2

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t):
    pass


def test():
    t = """
""".strip('\n')

    # assert solve(t) == 0

    # assert solve('') == 0


def getinput():
    import fileinput
    f = fileinput.input()
    text = ''.join(f).strip('\n')
    f.close()
    return text


if __name__ == '__main__':
    test()
    print(solve(getinput()))
