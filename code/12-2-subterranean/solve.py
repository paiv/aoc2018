#!/usr/bin/env python -O
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def solve(t, span=50000000000):
    ts = t.split()

    state = ts[2]
    ts = ts[3:]
    rules = dict(zip(ts[::3], ts[2::3]))

    trace(state)
    trace(rules)

    state = dict(enumerate(state))
    visited = set()

    for t in range(span):
        new_state = dict()
        for k in range(min(state)-2, max(state)+3):
            if rules.get(''.join(state.get(x, '.') for x in range(k-2, k+3)), '.') == '#':
                new_state[k] = '#'
        state = new_state

        trace(''.join(state.get(k, '.') for k in range(min(-4, min(state)), max(state)+1)))

        q = ''.join(state.get(k, '.') for k in range(min(state), max(state)+1))
        if q in visited:
            break
        visited.add(q)

    trace(min(state), max(state))

    dt = span - t - 1
    res = sum((k + dt) for k,v in state.items() if v == '#')
    trace(res)
    return res


def test():
    t = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".strip('\n')

    assert solve(t, span=20) == 325


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
