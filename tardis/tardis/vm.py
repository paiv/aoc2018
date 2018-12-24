

class Image:
    def __init__(self, program, rip=0, regs=None, ip=0):
        self.program = program
        self.rip = rip
        self.regs = regs or [0] * 6
        self.ip = ip


class TardisVM:
    def addi(a, b, c, regs):
        regs[c] = regs[a] + b
    def addr(a, b, c, regs):
        regs[c] = regs[a] + regs[b]
    def bani(a, b, c, regs):
        regs[c] = regs[a] & b
    def banr(a, b, c, regs):
        regs[c] = regs[a] & regs[b]
    def bori(a, b, c, regs):
        regs[c] = regs[a] | b
    def borr(a, b, c, regs):
        regs[c] = regs[a] | regs[b]
    def eqir(a, b, c, regs):
        regs[c] = 1 if a == regs[b] else 0
    def eqri(a, b, c, regs):
        regs[c] = 1 if regs[a] == b else 0
    def eqrr(a, b, c, regs):
        regs[c] = 1 if regs[a] == regs[b] else 0
    def gtir(a, b, c, regs):
        regs[c] = 1 if a > regs[b] else 0
    def gtri(a, b, c, regs):
        regs[c] = 1 if regs[a] > b else 0
    def gtrr(a, b, c, regs):
        regs[c] = 1 if regs[a] > regs[b] else 0
    def muli(a, b, c, regs):
        regs[c] = regs[a] * b
    def mulr(a, b, c, regs):
        regs[c] = regs[a] * regs[b]
    def seti(a, b, c, regs):
        regs[c] = a
    def setr(a, b, c, regs):
        regs[c] = regs[a]

    instr = dict(
        addi=addi, addr=addr,
        bani=bani, banr=banr,
        bori=bori, borr=borr,
        eqir=eqir, eqri=eqri, eqrr=eqrr,
        gtir=gtir, gtri=gtri, gtrr=gtrr,
        muli=muli, mulr=mulr,
        seti=seti, setr=setr,
    )

    INSTRUCTIONS = frozenset(instr.keys())

    def __init__(self, image):
        self.image = image

    def run(self):
        program = self.image.program
        regs = list(self.image.regs)
        rip = self.image.rip
        ip = self.image.ip
        instr = self.instr

        while 0 <= ip < len(program):
            regs[rip] = ip
            op, a, b, c = program[ip]
            instr[op](a, b, c, regs=regs)
            ip = regs[rip] + 1

        self.image = Image(program, rip=rip, regs=regs, ip=ip)

        return regs[0]
