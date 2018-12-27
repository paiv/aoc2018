from . import assembler as asm
from . import generators
from . import vm


class TardisError(Exception):
    pass


class BaseTardis:
    def __init__(self):
        self.asm = self._assembler()
        self.image = None

    def load(self, fp):
        self.asm.load(fp)

    def compile(self):
        self.image, errors = self.asm.compile()
        if errors:
            raise TardisError(errors)

    def emit(self, output=None):
        if not self.image:
            self.compile()

        gen = self._generator()
        gen.emit(self.image, output=output)

    def run(self):
        if not self.image:
            self.compile()

        vm = self._virtual_machine(self.image)
        vm.run()
        return vm

    def _assembler(self):
        return asm.Assembler()

    def _virtual_machine(self, image):
        return vm.TardisVM(image)

    def _generator(self):
        raise NotImplementedError()


class Tardis(BaseTardis):
    def _generator(self):
        return generators.GeneratorPy()


class TardisAsm(BaseTardis):
    def _generator(self):
        return generators.GeneratorCppAsm()


class TardisC(BaseTardis):
    def _generator(self):
        return generators.GeneratorDisasm()


def assemble_files(files, outfile, generator=None, verbose=False):
    tds = TardisC()

    if generator:
        generator = generator.lower()
        if generator == 'c-asm':
            tds = TardisAsm()
        elif generator == 'py':
            tds = Tardis()

    for fp in files:
        tds.load(fp)

    tds.emit(output=outfile)
