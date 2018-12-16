#!/usr/bin/env python
import re


def solve(t):
    samples, prog = t.rsplit('\n\n\n')

    t = [[*map(int, re.findall(r'-?\d+', s))]
        for s in samples.splitlines()]
    samples = [*zip(t[::4], t[1::4], t[2::4])]

    mem = list()

    def addr(a, b, c, mem=mem):
        mem[c] = mem[a] + mem[b]
    def addi(a, b, c, mem=mem):
        mem[c] = mem[a] + b
    def mulr(a, b, c, mem=mem):
        mem[c] = mem[a] * mem[b]
    def muli(a, b, c, mem=mem):
        mem[c] = mem[a] * b
    def banr(a, b, c, mem=mem):
        mem[c] = mem[a] & mem[b]
    def bani(a, b, c, mem=mem):
        mem[c] = mem[a] & b
    def borr(a, b, c, mem=mem):
        mem[c] = mem[a] | mem[b]
    def bori(a, b, c, mem=mem):
        mem[c] = mem[a] | b
    def setr(a, b, c, mem=mem):
        mem[c] = mem[a]
    def seti(a, b, c, mem=mem):
        mem[c] = a
    def gtir(a, b, c, mem=mem):
        mem[c] = 1 if a > mem[b] else 0
    def gtri(a, b, c, mem=mem):
        mem[c] = 1 if mem[a] > b else 0
    def gtrr(a, b, c, mem=mem):
        mem[c] = 1 if mem[a] > mem[b] else 0
    def eqir(a, b, c, mem=mem):
        mem[c] = 1 if a == mem[b] else 0
    def eqri(a, b, c, mem=mem):
        mem[c] = 1 if mem[a] == b else 0
    def eqrr(a, b, c, mem=mem):
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

    res = [reverse(*p) for p in samples]
    res = sum(len(x) > 2 for x in res)
    return res


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
