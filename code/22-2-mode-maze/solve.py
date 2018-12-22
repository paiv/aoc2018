#!/usr/bin/env python
import heapq
import re
from functools import lru_cache


def solve(t):
    depth, w, h = [*map(int, re.findall(r'-?\d+', t))]
    target = w + h * 1j

    @lru_cache(maxsize=None)
    def erosion(at):
        if (not at) or (at == target):
            return 0
        if not at.imag:
            return (int(at.real) * 16807 + depth) % 20183
        elif not at.real:
            return (int(at.imag) * 48271 + depth) % 20183
        else:
            return (erosion(at-1) * erosion(at-1j) + depth) % 20183

    def risk(at):
        return erosion(at) % 3

    NEI, GEAR, TORCH = range(3)
    usable = [{GEAR, TORCH}, {NEI, GEAR}, {NEI, TORCH}]

    def md(a, b):
        return abs(b.real - a.real) + abs(b.imag - a.imag)

    def heu(p, tool):
        return md(p, target) + (7 if tool != TORCH else 0)

    fringe = [(md(0, target), (0,0), TORCH, 0)]
    visited = set()

    while fringe:
        _, (x,y), tool, path = heapq.heappop(fringe)
        pos = x + y*1j

        if pos == target and tool == TORCH:
            break

        k = (pos, tool)
        if k in visited: continue
        visited.add(k)

        for tt in ({NEI, GEAR, TORCH} - {tool}):
            if tt in usable[risk(pos)]:
                heapq.heappush(fringe, (heu(pos, tt) + path + 7, (pos.real, pos.imag), tt, path + 7))

        for dr in (1, 1j, -1j, -1):
            tpos = pos + dr
            if tpos.real < 0 or tpos.imag < 0:
                continue
            if tool in usable[risk(tpos)]:
                heapq.heappush(fringe, (heu(tpos, tool) + path + 1, (tpos.real, tpos.imag), tool, path + 1))

    return path


def test():
    t = r"""
depth: 510
target: 10,10
""".strip('\n')

    assert solve(t) == 45


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
