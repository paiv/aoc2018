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


class TardisC(BaseTardis):
    def _generator(self):
        return generators.GeneratorCpp()


def assemble_files(files, outfile, verbose=False):
    tds = TardisC()

    for fp in files:
        tds.load(fp)

    tds.emit(output=outfile)
