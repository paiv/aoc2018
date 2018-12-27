import io
import re
from . import vm


class Assembler:

    class Input:
        _ids = 0

        def __init__(self, fp):
            self.fp = fp
            self.name = None
            if hasattr(fp, 'name'):
                self.name = fp.name
            if not self.name:
                self.name = '<{}>'.format(self._next_id())

        def _next_id(self):
            Assembler.Input._ids += 1
            return Assembler.Input._ids

        def __iter__(self):
            for line in self.fp:
                yield line

    def __init__(self):
        self.inputs = list()

    def load(self, fp):
        if isinstance(fp, str):
            fp = io.StringIO(fp)
        fin = Assembler.Input(fp)
        self.inputs.append(fin)

    def compile(self):
        instrs = '|'.join(vm.TardisVM.INSTRUCTIONS)
        rx = r'^ (?:[#]ip\s+ (?P<rip>\d+) | (?P<op>{instrs})\s+ (-?\d+)\s+ (-?\d+)\s+ (-?\d+)) $'.replace('{instrs}', instrs)
        rx = re.compile(rx, re.X)

        rip = None
        program = list()

        for src in self.inputs:
            for lineno, line in enumerate(src, 1):
                line = line.strip()
                if not line: continue

                m = rx.search(line)
                if not m:
                    error = '{}:{}  Invalid input {}'.format(src.name, lineno, repr(line))
                    return None, error

                if m.group('rip') is not None:
                    rip = int(m.group('rip'))

                elif m.group('op') is not None:
                    op = m.group('op')
                    a, b, c = map(int, [m.group(i) for i in (3, 4, 5)])
                    program.append((op, a, b, c))

        image = vm.Image(program, rip=rip)

        return image, None
