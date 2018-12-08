#!/usr/bin/env python -OO
from collections import defaultdict


def solve(t):
    rules = [(p[1] + p[7]) for line in t.splitlines() for p in [line.split()]]

    abc = set(x for p in rules for x in p)
    deps = defaultdict(set)

    for a,b in rules:
        deps[b].add(a)

    res = ''

    while abc:
        for k in sorted(abc):
            if not deps[k]:
                res += k
                abc.remove(k)
                for ds in deps.values():
                    ds.discard(k)
                break

    return res



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

    assert solve(t) == 'CABDFE'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
