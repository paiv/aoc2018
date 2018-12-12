#!/usr/bin/env python
import itertools


def solve(t):
    t = t.splitlines()

    for a, b in itertools.combinations(t, 2):
        if sum(x != y for x, y in zip(a, b)) == 1:
            s = set(a) & set(b)
            return ''.join(x for x in a if x in s)


def test():
    t = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
""".strip('\n')

    assert solve(t) == 'fgij', solve(t)


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
