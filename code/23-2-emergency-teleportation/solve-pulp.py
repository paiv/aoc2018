#!/usr/bin/env python -OO
import itertools
import pulp
import re
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def make_model(bots):
    model = pulp.LpProblem('Teleport', pulp.LpMaximize)

    bot_count = pulp.LpVariable('BotCount', lowBound=0, cat='Integer')
    model += bot_count

    X = pulp.LpVariable('X', cat='Integer')
    Y = pulp.LpVariable('Y', cat='Integer')
    Z = pulp.LpVariable('Z', cat='Integer')

    lp_bots = list()
    big = max(r for _,r in bots) * 10

    for i, ((x, y, z), r) in enumerate(bots):
        i_bot = pulp.LpVariable(f'bot_{i}', lowBound=0, upBound=1, cat='Integer')
        lp_bots.append(i_bot)

        for sx, sy, sz in itertools.product((-1, 1), repeat=3):
            model += ((sx * (x - X) + sy * (y - Y) + sz * (z - Z)) <= r + (1 - i_bot) * big)

    model += bot_count == sum(lp_bots)

    return model


def solve(t):
    bots = [((x,y,z),r)
        for s in t.splitlines()
        for x,y,z,r in [map(int, re.findall(r'-?\d+', s))]]

    model = make_model(bots)
    trace(model)

    model.solve()
    trace(pulp.LpStatus[model.status])

    if model.status != pulp.LpStatusOptimal:
        print(pulp.LpStatus[model.status], file=sys.stderr)
        return

    vars = model.variablesDict()
    trace([abs(vars[k].varValue) for k in 'XYZ'])

    res = sum(int(abs(pulp.value(vars[k]))) for k in 'XYZ')

    trace(res)
    return res


def test():
    t = r"""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""".strip('\n')

    assert solve(t) == 36


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
