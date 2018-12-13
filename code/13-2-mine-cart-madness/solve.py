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
    carts = [(k, dirs[v], 0, i) for i, (k, v) in enumerate(carts.items())]

    turns = (-1j, 1, 1j)

    curves = {
        '\\': dict(zip([1, -1j, -1, 1j], [1j, -1, -1j, 1])),
        '/':  dict(zip([1, -1j, -1, 1j], [-1j, 1, 1j, -1])),
        }

    while len(carts) > 1:
        next_carts = list()
        hits = set(p for p, *_ in carts)
        collid = set()

        for pos, dr, turn, id in sorted(carts, key=lambda p: (p[0].imag, p[0].real)):
            hits.discard(pos)
            pos += dr

            if pos in hits:
                collid |= {id} | set(id for p,_,_,id in carts + next_carts if p == pos)
                hits.remove(pos)
            else:
                hits.add(pos)

            t = track[pos]

            if t == '+':
                dr *= turns[turn]
                turn = (turn + 1) % len(turns)
            elif t in '\\/':
                dr = curves[t][dr]

            next_carts.append((pos, dr, turn, id))

        carts = [(p,dr,h,id) for p, dr, h, id in next_carts if id not in collid]

    pos, *_ = carts[0]
    res = f'{int(pos.real)},{int(pos.imag)}'
    return res


def test():
    t = r"""
/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
""".strip('\n')

    assert solve(t) == '6,4'


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
