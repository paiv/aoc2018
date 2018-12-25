#!/usr/bin/env pypy3
import re
import sys


VERBOSE = 2 if __debug__ else 1

def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


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
            n, hp, ts, atk, ats, ni = (m.group(i) for i in range(1,7))
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
        dmg = ag['size'] * (ag['atk'])
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

    def battle(groups, boost):
        prev = dict()
        for k,g in groups.items():
            g = dict(g)
            aboo = (boost if g['army'] == IMMSYS else 0)
            g['atk'] += aboo
            prev[k] = g

        groups, prev = prev, None

        while groups:
            if groups == prev: break
            prev = {k:dict(g) for k,g in groups.items()}

            targets = dict()
            for ag in sorted(groups.values(), key=bypower):
                for _, _, _, bgid in sorted(estimate_attacks(ag, groups), reverse=True):
                    if bgid not in targets.values():
                        targets[ag['id']] = bgid
                        break

            if not targets: break

            for ag in sorted(groups.values(), key=byinitiative):
                bgid = targets.get(ag['id'])
                if bgid:
                    bg = groups[bgid]
                    dmg = attack_damage(ag, bg)
                    n, hp = bg['size'], bg['hp']
                    bg['size'] = max(0, n * hp - dmg + hp - 1) // hp

            groups = dict((k,g) for k, g in groups.items() if g['size'])

        armies = set(g['army'] for g in groups.values())
        army = armies.pop() if len(armies) == 1 else None
        size = sum(g['size'] for g in groups.values())
        return (army, size)


    if 0:
        lo = hi = boost = 0
        winner = None
        while not (winner == IMMSYS and lo == hi):
            trace('boost', boost)
            winner, res = battle(groups, boost)
            if winner == IMMSYS:
                hi = boost
                boost = (lo + hi) // 2
            elif not hi:
                lo = boost
                boost = 1 if not boost else boost * 2
            else:
                lo = boost + 1
                boost = (lo + hi) // 2

    else:
        winner = boost = 0
        best = float('inf')
        for boost in range(129):
            winner, res = battle(groups, boost)
            if winner == IMMSYS: best = min(best, boost)
            trace('=%.'[winner or 0], end='', flush=True)
        trace()
        trace('boost', best)

    return res


if __name__ == '__main__':
    if 1:
        import fileinput
        with fileinput.input() as f:
            text = ''.join(f).strip('\n')

        print(solve(text))

    else:
        import glob
        for fn in sorted(glob.glob('data/*.txt')):
            with open(fn) as f:
                print(fn[5:7], end=': ', flush=True)
                solve(f.read())
