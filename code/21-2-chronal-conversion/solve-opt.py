#!/usr/bin/env python
import sys
import tardis


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(files):
    tds = tardis.TardisC()
    for fp in files:
        tds.load(fp)

    tds.compile()
    # tds.image.regs[0] = 1

    tds.emit(output=sys.stdout)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='*', default=[sys.stdin], type=argparse.FileType('r'))
    args = parser.parse_args()

    solve(args.file)
