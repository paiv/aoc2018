#!/usr/bin/env python -OO
import re


def solve(t):
    n, w = map(int, re.findall(r'-?\d+', t))

    res = [0]
    off = 0
    score = [0] * n
    for x in range(1, w + 1):
        p = (x - 1) % n

        if x % 23 == 0:
            off = (off - 7) % len(res)
            q = res.pop(off)
            score[p] += (x + q)
            off = off % len(res)
        else:
            off = (off + 2) % len(res)
            if not off: off = len(res)
            res.insert(off, x)

    return max(score)


def test():
    assert solve('9 players; last marble is worth 25 points') == 32
    assert solve('10 players; last marble is worth 1618 points') == 8317
    assert solve('13 players; last marble is worth 7999 points') == 146373
    assert solve('17 players; last marble is worth 1104 points') == 2764
    assert solve('21 players; last marble is worth 6111 points') == 54718
    assert solve('30 players; last marble is worth 5807 points') == 37305


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
