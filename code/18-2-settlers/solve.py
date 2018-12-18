#!/usr/bin/env python

def solve(t):
    grid = {(x + y * 1j):v
        for y, row in enumerate(t.splitlines())
        for x, v in enumerate(row)
        if v in '.#|'}

    bx = int(max(p.real for p in grid))
    by = int(max(p.imag for p in grid))

    rounds = [grid]

    for t in range(1, 1000000000):
        next_grid = dict()
        for y in range(by+1):
            for x in range(bx+1):
                pos = x + y*1j
                c = grid.get(pos, '.')

                ya = te = 0
                for a in (-1, 0, 1):
                    for b in (-1j, 0, 1j):
                        d = a + b
                        if d:
                            q = grid.get(pos + d, '.')
                            te += q == '|'
                            ya += q == '#'

                if c == '.':
                    if te >= 3:
                        next_grid[pos] = '|'
                elif c == '|':
                    next_grid[pos] = '#' if ya >= 3 else '|'
                elif c == '#':
                    if (ya > 0 < te):
                        next_grid[pos] = '#'

        grid = next_grid

        if grid in rounds: break
        rounds.append(grid)

    a, = [i for i, x in enumerate(rounds) if x == grid]

    grid = rounds[a + (1000000000 - a) % (t - a)]

    ts = sum(x == '|' for x in grid.values())
    ns = sum(x == '#' for x in grid.values())
    return ts * ns


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
