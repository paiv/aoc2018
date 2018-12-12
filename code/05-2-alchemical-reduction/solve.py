#!/usr/bin/env python -OO
import string


def solve(t):

    def react(s, k):
        dx = ord('a') - ord('A')
        ks = (k, k+dx)
        q = list()
        for x in map(ord, s):
            if x in ks: continue
            if q and abs(q[-1] - x) == dx:
                q.pop()
            else:
                q.append(x)
        return q

    best = len(t)
    for k in map(ord, string.ascii_uppercase):
        q = react(t, k)
        best = min(best, len(q))

    return best


def test():
    assert solve('dabAcCaCBAcCcaDA') == 4


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
