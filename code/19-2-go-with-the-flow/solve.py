#!/usr/bin/env python


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
    def setr(a, b, c, mem):
        mem[c] = mem[a]
    def seti(a, b, c, mem):
        mem[c] = a
    def gtrr(a, b, c, mem):
        mem[c] = 1 if mem[a] > mem[b] else 0
    def eqrr(a, b, c, mem):
        mem[c] = 1 if mem[a] == mem[b] else 0

    instrs = dict(
        addr=addr, addi=addi,
        mulr=mulr, muli=muli,
        setr=setr, seti=seti,
        eqrr=eqrr, gtrr=gtrr,
    )

    mem = [0] * 6
    mem[0] = 1
    ip = 0

    while 0 <= ip < len(prog):
        if ip == 1: break

        mem[rip] = ip
        op, a, b, c = prog[ip]
        instrs[op](a, b, c, mem=mem)
        ip = mem[rip] + 1

    return sum(factors(mem[2]))


def factors(x):
    res = set()
    for i in range(1, int(x ** 0.5) + 1):
        d, r = divmod(x, i)
        if r == 0:
            res |= {i, d}
    return res


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
