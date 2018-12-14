#!/usr/bin/env pypy3


def solve(t):
    query = [*map(int, t.strip())]
    nq = len(query)

    m = [3, 7]
    a, b = 0, 1

    while query not in (m[-nq:], m[-nq-1:-1]):
        s = m[a] + m[b]
        m.extend((s,) if s < 10 else divmod(s, 10))
        a = (a + m[a] + 1) % len(m)
        b = (b + m[b] + 1) % len(m)

    res = len(m) - nq - (m[-nq:] != query)
    return res


def test():
    assert solve('01245') == 5
    assert solve('51589') == 9
    assert solve('92510') == 18
    assert solve('59414') == 2018


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
