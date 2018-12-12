#!/usr/bin/env python
import itertools


def solve(t):
    xs = map(int, t.replace(',', ' ').split())
    seen = set()
    t = 0
    for x in itertools.cycle(xs):
        if t in seen:
            return t
        seen.add(t)
        t += x


def test():
    assert solve('+1, -2, +3, +1') == 2
    assert solve('+1, -1') == 0
    assert solve('+3, +3, +4, -2, -4') == 10
    assert solve('-6, +3, +8, +5, -6') == 5
    assert solve('+7, +7, -2, -7, -4') == 14


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
