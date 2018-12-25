#!/usr/bin/env pypy3 -OO
import itertools
import re
import sys
from collections import defaultdict


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def md(a, b):
    return sum(abs(x - y) for x,y in zip(a, b))


def solve(t):
    points = [tuple(map(int, re.findall(r'-?\d+', s)))
        for s in t.splitlines()]

    edges = defaultdict(set)

    for a, b in itertools.combinations(range(len(points)), 2):
        d = md(points[a], points[b])
        if d <= 3:
            edges[a].add(b)
            edges[b].add(a)

    components = 0
    visited = set()

    for pos in range(len(points)):
        if pos in visited: continue
        cc = set()
        fringe = [pos]
        while fringe:
            p = fringe.pop()
            if p in visited: continue
            cc.add(p)
            visited.add(p)
            for q in edges.get(p, set()):
                fringe.append(q)
        trace(cc)
        components += 1

    trace(components)
    return components


def test():
    t = r"""
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
""".strip('\n')

    assert solve(t) == 2

    t = r"""
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
""".strip('\n')

    assert solve(t) == 4

    t = r"""
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
""".strip('\n')

    assert solve(t) == 3

    t = r"""
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
""".strip('\n')

    assert solve(t) == 8

    trace('OK')


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
