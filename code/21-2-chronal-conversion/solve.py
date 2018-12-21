#!/usr/bin/env pypy3 -O


def solve(t):
    prog = t.splitlines()
    rip = int(prog[0].split()[-1])
    prog = [(op, *map(int, xs)) for s in prog[1:] for op, *xs in [s.split()]]

    def addr(a, b, c, mem):
        mem[c] = mem[a] + mem[b]
    def addi(a, b, c, mem):
        mem[c] = mem[a] + b
    def bani(a, b, c, mem):
        mem[c] = mem[a] & b
    def bori(a, b, c, mem):
        mem[c] = mem[a] | b
    def eqri(a, b, c, mem):
        mem[c] = 1 if mem[a] == b else 0
    def eqrr(a, b, c, mem):
        mem[c] = 1 if mem[a] == mem[b] else 0
    def gtir(a, b, c, mem):
        mem[c] = 1 if a > mem[b] else 0
    def gtrr(a, b, c, mem):
        mem[c] = 1 if mem[a] > mem[b] else 0
    def muli(a, b, c, mem):
        mem[c] = mem[a] * b
    def seti(a, b, c, mem):
        mem[c] = a
    def setr(a, b, c, mem):
        mem[c] = mem[a]

    instrs = dict(
        addi=addi, addr=addr,
        bani=bani, bori=bori,
        eqri=eqri, eqrr=eqrr,
        gtir=gtir, gtrr=gtrr,
        muli=muli,
        seti=seti, setr=setr
    )

    mem = [0] * 6
    ip = 0
    res = None
    visited = set()

    while 0 <= ip < len(prog):
        # part 2
        if ip == 29:
            if mem[5] in visited:
                break
            res = mem[5]
            visited.add(res)

        mem[rip] = ip
        op, a, b, c = prog[ip]
        instrs[op](a, b, c, mem=mem)
        ip = mem[rip] + 1

    return res


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
