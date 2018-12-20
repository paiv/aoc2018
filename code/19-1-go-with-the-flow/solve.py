#!/usr/bin/env pypy3 -OO


def solve(t):
    prog = t.splitlines()
    rip = int(prog[0].split()[-1])
    prog = [(op, *map(int, xs)) for s in prog[1:] for op, *xs in [s.split()]]

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

    mem = [0] * 6
    ip = mem[rip]

    while 0 <= ip < len(prog):
        mem[rip] = ip
        op, a, b, c = prog[ip]
        instrs[op](a, b, c, mem=mem)
        ip = mem[rip] + 1

    return mem[0]


def test():
    t = r"""
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".strip('\n')

    assert solve(t) == 6


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
