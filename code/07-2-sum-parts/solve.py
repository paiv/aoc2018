#!/usr/bin/env python -OO
import string
import sys
from collections import defaultdict


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t, nworkers=5, baseline=61):
    rules = [(p[1] + p[7]) for line in t.splitlines() for p in [line.split()]]
    trace(rules)

    abc = set(x for p in rules for x in p)
    deps = defaultdict(set)

    for a,b in rules:
        deps[b].add(a)

    trace(deps)

    ticks = 0
    workers = []
    res = ''
    hi = string.ascii_uppercase

    while abc or workers:
        for k in sorted(abc):
            if len(workers) >= nworkers:
                break
            if not deps[k]:
                abc.remove(k)
                workers.append((k, hi.index(k) + baseline))

        done = [k for k,t in workers if t <= 1]
        workers = [(k, t - 1) for k,t in workers if t > 1]

        for k in done:
            res += k
            for ds in deps.values():
                ds.discard(k)

        ticks += 1

    trace(res)
    return ticks



def test():
    t = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip('\n')

    assert solve(t, nworkers=2, baseline=1) == 15


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
