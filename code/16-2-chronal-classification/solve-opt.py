#!/usr/bin/env python -O
import re
import tardis
from collections import defaultdict


def solve(t):
    samples, prog = t.rsplit('\n\n\n')

    t = [[*map(int, re.findall(r'-?\d+', s))]
        for s in samples.splitlines()]
    samples = [*zip(t[::4], t[1::4], t[2::4])]

    prog = [[*map(int, re.findall(r'-?\d+', s))]
        for s in prog.splitlines()]

    def addr(a, b, c, mem):
        mem[c] = mem[a] + mem[b]
    def addi(a, b, c, mem):
        mem[c] = mem[a] + b
    def mulr(a, b, c, mem):
        mem[c] = mem[a] * mem[b]
    def muli(a, b, c, mem):
        mem[c] = mem[a] * b
    def banr(a, b, c, mem):
        mem[c] = mem[a] & mem[b]
    def bani(a, b, c, mem):
        mem[c] = mem[a] & b
    def borr(a, b, c, mem):
        mem[c] = mem[a] | mem[b]
    def bori(a, b, c, mem):
        mem[c] = mem[a] | b
    def setr(a, b, c, mem):
        mem[c] = mem[a]
    def seti(a, b, c, mem):
        mem[c] = a
    def gtir(a, b, c, mem):
        mem[c] = 1 if a > mem[b] else 0
    def gtri(a, b, c, mem):
        mem[c] = 1 if mem[a] > b else 0
    def gtrr(a, b, c, mem):
        mem[c] = 1 if mem[a] > mem[b] else 0
    def eqir(a, b, c, mem):
        mem[c] = 1 if a == mem[b] else 0
    def eqri(a, b, c, mem):
        mem[c] = 1 if mem[a] == b else 0
    def eqrr(a, b, c, mem):
        mem[c] = 1 if mem[a] == mem[b] else 0

    instrs = dict(
        addr=addr, addi=addi,
        mulr=mulr, muli=muli,
        banr=banr, bani=bani,
        borr=borr, bori=bori,
        setr=setr, seti=seti,
        gtir=gtir, gtri=gtri, gtrr=gtrr,
        eqir=eqir, eqri=eqri, eqrr=eqrr,
    )

    def reverse(before, instr, after):
        res = set()
        for k, op in instrs.items():
            mem = list(before)
            op(*instr[1:], mem=mem)
            if mem == after:
                res.add(k)
        return res

    alts = defaultdict(set)
    for p in samples:
        _,(op,*_),_ = p
        alts[op] |= reverse(*p)

    while alts:
        op, (name,) = next((op, ns) for op, ns in alts.items() if len(ns) == 1)
        instrs[op] = instrs[name]
        alts = {op:(ns - {name}) for op, ns in alts.items() if ns != {name}}

    names = {i:instrs[i].__name__ for i in range(16)}

    prog = '\n'.join(f'{names[op]} {a} {b} {c}' for op, a, b, c in prog)
    prog = f"""
#ip 5
{prog}
""".strip()

    tds = tardis.TardisC()
    tds.load(prog)
    source = tds.emit()
    print(source)


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    solve(text)
