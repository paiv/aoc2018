#!/usr/bin/env pypy3


def solve(t):
    N = int(t)

    m = [3, 7]
    a, b = 0, 1

    while len(m) < N + 10:
        s = m[a] + m[b]
        m.extend((s,) if s < 10 else divmod(s, 10))
        a = (a + m[a] + 1) % len(m)
        b = (b + m[b] + 1) % len(m)

    res = ''.join(map(str, m[N:N+10]))
    return res


def test():
    assert solve('5') == '0124515891'
    assert solve('9') == '5158916779'
    assert solve('18') == '9251071085'
    assert solve('2018') == '5941429882'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
