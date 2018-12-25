#!/usr/bin/env python
import copy
import io
import re
import time
from collections import Counter


IMMSYS, INFECT = 1, 2


def dump(groups, battle):
    groups = sorted(groups.items())
    imms = [(gid, g) for gid,g in groups if g['army'] == IMMSYS]
    infs = [(gid, g) for gid,g in groups if g['army'] == INFECT]

    def print_groups(so, gs):
        if gs:
            for k, g in gs:
                gid, n = g['id'][1], g['size']
                s = '' if n == 1 else 's'
                print(f'Group {gid} contains {n} unit{s}', file=so)
        else:
            print('No groups remain.', file=so)

    with io.StringIO() as so:
        print('Immune System:', file=so)
        print_groups(so, imms)
        print('Infection:', file=so)
        print_groups(so, infs)
        print('', file=so)

        for a, b, kia in battle:
            ak, aid = a
            bk, bid = b
            army = 'Immune System' if ak == IMMSYS else 'Infection'
            s = '' if kia == 1 else 's'
            t = f'{army} group {aid} attacks defending group {bid}, killing {kia} unit{s}'
            print(t, file=so)
        print(so.getvalue())


def solve(t, boost=0):
    rx = re.compile(r'(\d+) units each with (\d+) hit points(?: \((.*?)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    army = None
    groups = dict()
    ids = Counter()

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
            ids[army] += 1
            gid = (army, ids[army])
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


    prev = dict()
    for k,g in groups.items():
        g = dict(g)
        boo = (boost if g['army'] == IMMSYS else 0)
        g['atk'] += boo
        prev[k] = g

    groups, prev = prev, None

    while groups:
        record_start = copy.deepcopy(groups)
        record_battle = list()

        if groups == prev: break
        prev = copy.deepcopy(groups)

        targets = dict()
        for ag in sorted(groups.values(), key=bypower):
            for _, _, _, bgid in sorted(estimate_attacks(ag, groups), reverse=True):
                if bgid not in targets.values():
                    targets[ag['id']] = bgid
                    break

        if not targets: break

        for ag in sorted(groups.values(), key=byinitiative):
            if not ag['size']: continue
            bgid = targets.get(ag['id'])
            if bgid:
                bg = groups[bgid]
                dmg = attack_damage(ag, bg)
                n, hp = bg['size'], bg['hp']
                kia = min(n, dmg // hp)
                bg['size'] = n - kia
                record_battle.append((ag['id'], bgid, kia))

        groups = dict((k,g) for k, g in groups.items() if g['size'])

        yield (record_start, record_battle)

    record_start = copy.deepcopy(groups)
    record_battle = list()
    yield (record_start, record_battle)

    armies = set(g['army'] for g in groups.values())
    army = armies.pop() if len(armies) == 1 else None
    size = sum(g['size'] for g in groups.values())

    print('winner:', army, 'size:', size)


def viz(file, boost=0, rate=1):
    text = file.read()

    for frame in solve(text, boost=boost):
        dump(*frame)
        time.sleep(1/rate)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Input file')
    parser.add_argument('-b', '--boost', default=0, type=int, help='Boost immune system')
    parser.add_argument('-r', '--rate', default=3, type=float, help='Frame rate')
    args = parser.parse_args()

    viz(file=args.file, rate=args.rate, boost=args.boost)
