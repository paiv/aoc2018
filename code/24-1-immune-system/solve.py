#!/usr/bin/env python -OO
import re
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


class somed(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def solve(t):
    rx = re.compile(r'(\d+) units each with (\d+) hit points(?: \((.*?)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    IMMSYS, INFECT = 1, 2
    army = None
    groups = dict()

    for s in t.splitlines():
        if s == 'Immune System:':
            army = IMMSYS
        elif s == 'Infection:':
            army = INFECT
        elif s and s[0].isdigit():
            m = rx.match(s)
            n, hp, ts, atk, ats, ni = (m[i] for i in range(1,7))
            n, hp, atk, ni = map(int, (n, hp, atk, ni))
            dts = dict((s.split()[0], tuple(x.strip(',') for x in s.split()[2:])) for s in ts.split(';')) if ts else dict()
            weak = frozenset(dts.get('weak', tuple()))
            immune = frozenset(dts.get('immune', tuple()))
            gid = len(groups)+1
            groups[gid] = dict(army=army, id=gid, size=n, hp=hp,
                weak=weak, immune=immune, atk=atk, typeatk=ats, initiative=ni)

    def bypower(g):
        pwr, ni = g['size'] * g['atk'], g['initiative']
        return (-pwr, -ni)

    def byinitiative(g):
        return -g['initiative']

    def attack_damage(ag, bg):
        dmg = ag['size'] * ag['atk']
        tatk = ag['typeatk']

        if tatk in bg['immune']:
            dmg = 0
        elif tatk in bg['weak']:
            dmg *= 2
        return dmg

    def estimate_attacks(g, groups):
        targets = list()
        tatk = g['typeatk']
        for bg in groups.values():
            if g['army'] != bg['army'] and bg['size']:
                dmg = attack_damage(g, bg)
                if dmg > 0:
                    bpwr, bni = bg['size'] * bg['atk'], bg['initiative']
                    targets.append((dmg, bpwr, bni, bg['id']))
        return targets

    while groups:
        trace(groups)

        targets = dict()
        for ag in sorted(groups.values(), key=bypower):
            for _, _, _, bgid in sorted(estimate_attacks(ag, groups), reverse=True):
                if bgid not in targets.values():
                    targets[ag['id']] = bgid
                    break

        trace('targets', targets)
        if not targets: break

        for ag in sorted(groups.values(), key=byinitiative):
            bgid = targets.get(ag['id'])
            if bgid:
                bg = groups[bgid]
                trace(ag['id'], '->', bgid)

                dmg = attack_damage(ag, bg)
                n, hp = bg['size'], bg['hp']
                bg['size'] = max(0, n * hp - dmg + hp - 1) // hp

        groups = dict((k,g) for k, g in groups.items() if g['size'])

    res = sum(g['size'] for g in groups.values())
    trace(res)
    return res


def test():
    t = r"""
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".strip('\n')

    assert solve(t) == 5216


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
