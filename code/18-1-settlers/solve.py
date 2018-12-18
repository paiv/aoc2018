#!/usr/bin/env python


def around(pos, grid):
    return [grid.get(pos + d, '.')
        for a in (-1, 0, 1) for b in (-1j, 0, 1j)
        for d in [a + b] if d]


def evolve(pos, grid):
    c = grid.get(pos, '.')
    if c == '.':
        return '|' if around(pos, grid).count('|') >= 3 else '.'
    elif c == '|':
        return '#' if around(pos, grid).count('#') >= 3 else '|'
    elif c == '#':
        r = around(pos, grid)
        ns, ts = r.count('#'), r.count('|')
        return '#' if (ns > 0 < ts) else '.'


def solve(t):
    grid = {(x + y * 1j):v
        for y, row in enumerate(t.splitlines())
        for x, v in enumerate(row)
        if v in '.#|'}

    bx = int(max(p.real for p in grid))
    by = int(max(p.imag for p in grid))

    for _ in range(10):
        next_grid = dict(grid)
        for y in range(by+1):
            for x in range(bx+1):
                pos = x + y*1j
                next_grid[pos] = evolve(pos, grid)
        grid = next_grid

    ts = sum(x == '|' for x in grid.values())
    ns = sum(x == '#' for x in grid.values())
    return ts * ns


def test():
    t = r"""
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".strip('\n')

    assert solve(t) == 1147


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
