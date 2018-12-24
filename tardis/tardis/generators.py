import jinja2
from . import vm


class BaseGenerator:
    templates_dir = 'templates'

    def emit(self, image, output):

        env = jinja2.Environment(
            loader=jinja2.PackageLoader(self.__module__, self.templates_dir)
        )

        tpl = env.get_template(self.template_name)

        model = self._transpile(image)

        for text in tpl.generate(model):
            print(text, end='', file=output)
        print('', file=output)


class Generator(BaseGenerator):
    def _transpile(self, image):
        instr = sorted(set(line[0] for line in image.program))

        program = [(instr.index(line[0]), *line[1:]) for line in image.program]

        return dict(
            instructions=instr,
            program=program,
            registers=image.regs,
            rip=image.rip,
            ip=image.ip,
        )


class GeneratorPy(Generator):
    template_name = 'program.py'


class GeneratorCppDispatch(Generator):
    template_name = 'dispatch.cpp'


class GeneratorCpp(BaseGenerator):
    template_name = 'program.cpp'

    def _transpile(self, image):
        rip = image.rip
        ip = image.ip
        regs = {f'r{i}': x for i, x in enumerate(image.regs)}

        program = list()

        def emit(line, semi=False):
            sep = ';' if semi else ''
            program.append(f'{line}{sep}')

        def cond(i, a, cmp, b, c):
            xop, xa, xb, xc = image.program[i + 1]
            if xc == rip and xop == 'addr' and c in (xa, xb) and rip in (xa, xb):
                return f'if (!({a} {cmp} {b}))', True
            else:
                return f'r{c} = {a} {cmp} {b}', False

        if ip:
            emit(f'goto src{ip}')

        for i, (op, a, b, c) in enumerate(image.program):
            emit(f'// {i:3}: {op} {a} {b} {c}')
            semi = True

            def getr(x):
                if x == rip: return i
                else: return f'r{x}'

            if op == 'addi':
                if c == rip:
                    if a == rip:
                        instr = f'goto src{i + b + 1}'
                    else:
                        raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} + {b}'

            elif op == 'addr':
                if c == rip:
                    prev = b if a == rip else a if b == rip else None
                    xop, xa, xb, xc = image.program[i - 1]
                    if xc != prev:
                        emit('// WARN:')
                    instr = f'if (!r{prev})'
                    semi = False
                else:
                    instr = f'r{c} = {getr(a)} + {getr(b)}'

            elif op == 'bani':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} & {b}'

            elif op == 'banr':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} & {getr(b)}'

            elif op == 'bori':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} | {b}'

            elif op == 'borr':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} | {getr(b)}'

            elif op == 'eqir':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {a} == {getr(b)} ? 1 : 0'

            elif op == 'eqri':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} == {b} ? 1 : 0'

            elif op == 'eqrr':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} == {getr(b)} ? 1 : 0'

            elif op == 'gtir':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {a} > {getr(b)} ? 1 : 0'

            elif op == 'gtri':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} > {b} ? 1 : 0'

            elif op == 'gtrr':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} > {getr(b)} ? 1 : 0'

            elif op == 'muli':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} * {b}'

            elif op == 'mulr':
                if a == b == c == rip:
                    instr = 'goto srcexit'
                elif c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)} * {getr(b)}'

            elif op == 'seti':
                if c == rip:
                    instr = f'goto src{a + 1}'
                else:
                    instr = f'r{c} = {a}'

            elif op == 'setr':
                if c == rip:
                    raise Exception()
                else:
                    instr = f'r{c} = {getr(a)}'

            emit(f'src{i}: {instr}', semi=semi)

        emit(f'srcexit:')

        return dict(
            registers=regs,
            program=program,
        )
