#!/usr/bin/env python
from collections import Counter


def solve(t):
    def chks(s):
        v = Counter(s).values()
        return (2 in v, 3 in v)

    a, b = map(sum, zip(*map(chks, t.splitlines())))
    return a * b


def test():
    t = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
""".strip('\n')

    assert solve(t) == 12


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
