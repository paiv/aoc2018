#!/usr/bin/env python -OO
import string


def solve(t):
    dx = ord('a') - ord('A')
    q = list()
    for x in map(ord, t):
        if q and abs(q[-1] - x) == dx:
            q.pop()
        else:
            q.append(x)
    return len(q)

    # while t:
    #     r = t
    #     for a, b in zip(string.ascii_lowercase, string.ascii_uppercase):
    #         r = r.replace(a+b, '').replace(b+a, '')
    #     if r == t: break
    #     t = r
    # return len(t)


def test():
    assert solve('aA') == 0
    assert solve('abBA') == 0
    assert solve('abAB') == 4
    assert solve('aabAAB') == 6
    assert solve('dabAcCaCBAcCcaDA') == 10


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
