#!/usr/bin/env python -O


def solve(t):
    track = {(y*1j + x):v
        for y, row in enumerate(t.splitlines())
        for x, v in enumerate(row)
        if not v.isspace()}

    carts = {k:v for k,v in track.items() if v in '<>^v'}

    for k, v in carts.items():
        track[k] = '-' if v in '<>' else '|'

    dirs = dict(zip('<>^v', (-1, 1, -1j, 1j)))
    carts = [(k, dirs[v], 0) for k, v in carts.items()]

    turns = (-1j, 1, 1j)

    curves = {
        '\\': dict(zip([1, -1j, -1, 1j], [1j, -1, -1j, 1])),
        '/':  dict(zip([1, -1j, -1, 1j], [-1j, 1, 1j, -1])),
        }

    while True:
        next_carts = list()
        hits = set(p for p, *_ in carts)

        for pos, dr, turn in sorted(carts, key=lambda p: (p[0].imag, p[0].real)):
            hits.remove(pos)
            pos += dr

            if pos in hits:
                res = f'{int(pos.real)},{int(pos.imag)}'
                return res

            t = track[pos]

            if t == '+':
                dr *= turns[turn]
                turn = (turn + 1) % len(turns)

            elif t in '\\/':
                dr = curves[t][dr]

            next_carts.append((pos, dr, turn))
            hits.add(pos)

        carts = next_carts


def test():
    t = r"""
|
v
|
|
|
^
|
""".strip('\n')

    assert solve(t) == '0,3'

    t = r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
""".strip('\n')

    assert solve(t) == '7,3'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
