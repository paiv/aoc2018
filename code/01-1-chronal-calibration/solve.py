#!/usr/bin/env python

def solve(t):
    return sum(map(int, t.split()))


def test():
    assert solve('+1 -2 +3 +1') == 3
    assert solve('+1 +1 +1') == 3
    assert solve('+1 +1 -2') == 0
    assert solve('-1 -2 -3') == -6


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
