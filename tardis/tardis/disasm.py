import copy
import io


class TardisDisasm:
    def process(self, image, output=None):
        regs = image.regs
        rip = image.rip
        ip = image.ip

        state = [(f'ln{i}', xo) for i, xo in enumerate(image.program)]

        state = self._name_regs(image, state)
        state = self._c_expr(image, state)
        state = self._c_reduce(image, state)
        state = self._ip_const(image, state)
        state = self._ip_jump(image, state)
        state = self._expr_tree(image, state)
        state = self._if0(image, state)
        state = self._if_reduce(image, state)
        state = self._at_exit(image, state)
        state = self._generate(image, state, output=output)

        return state

    def _name_regs(self, image, state):
        rip = image.rip
        opsra = set('addi addr bani banr bori borr eqri eqrr gtri gtrr muli mulr setr'.split())
        opsrb = set('addr banr borr eqir eqrr gtir gtrr mulr'.split())

        def name_regs(op, a, b, c):
            if op in opsra:
                a = 'ip' if a == rip else f'r{a}'
            if op in opsrb:
                b = 'ip' if b == rip else f'r{b}'
            c = 'ip' if c == rip else f'r{c}'
            return (op, a, b, c)

        state = [(l, name_regs(*xo)) for l, xo in state]
        return state

    def _c_expr(self, image, state):
        def expr(op, a, b, c):
            if op in ('addi', 'addr'):
                return (c, '=', (a, '+', b))
            elif op in ('bani', 'banr'):
                return (c, '=', (a, '&', b))
            elif op in ('bori', 'borr'):
                return (c, '=', (a, '|', b))
            elif op in ('eqir', 'eqri', 'eqrr'):
                return (c, '=', (a, '==', b))
            elif op in ('gtir', 'gtri', 'gtrr'):
                return (c, '=', (a, '>', b))
            elif op in ('muli', 'mulr'):
                return (c, '=', (a, '*', b))
            elif op in ('seti', 'setr'):
                return (c, '=', a)

        state = [(l, expr(*xo)) for l, xo in state]
        return state

    def _c_reduce(self, image, state):
        mops = set('+*&|')

        def expr(a, op, b):
            if op == '=' and isinstance(b, tuple):
                x, xop, y = b
                if xop in mops:
                    if a == x:
                        return (a, f'{xop}=', y)
                    elif a == y:
                        return (a, f'{xop}=', x)
            return (a, op, b)

        state = [(l, expr(*xo)) for l, xo in state]
        return state

    def _ip_const(self, image, state):
        def expr(i, a, op, b):
            if b == 'ip':
                return (a, op, i)
            return (a, op, b)

        state = [(l, expr(i, *xo)) for i, (l, xo) in enumerate(state)]
        return state

    def _ip_jump(self, image, state):
        def expr(i, a, op, b):
            if a == 'ip' and isinstance(b, int):
                goto = None
                if op == '=':
                    goto = b + 1
                elif op == '+=':
                    goto = i + b + 1
                elif op == '*=':
                    goto = i * b + 1
                if goto >= len(state):
                    goto = 'exit'
                return (None, 'goto', (goto, f'ln{goto}'))
            return (a, op, b)

        state = [(l, expr(i, *xo)) for i, (l, xo) in enumerate(state)]
        return state

    def _expr_tree(self, image, state):
        def expr(sop):
            if isinstance(sop, int):
                return ConstExpr(sop)
            elif isinstance(sop, str):
                return VarExpr(sop)

            a, op, b = sop

            if op == '=':
                return AssignExpr(a, expr(b))
            elif op in ('+=', '*=', '&=', '|='):
                return OpAssignExpr(a, op[0], expr(b))
            elif op in ('+', '*', '&', '|', '==', '>'):
                return BinaryExpr(expr(a), op, expr(b))
            elif op == 'goto':
                return GotoExpr(*b)
            else:
                raise Exception((i, l, a, op, b))

        def texp(i, l, a, op, b):
            x = expr((a, op, b))
            x.source = ExprSource(line=i, instr=image.program[i])
            x.label = l
            return x

        prog = BlockExpr()
        for i, (l, op) in enumerate(state):
            prog.append(texp(i, l, *op))

        return prog

    def _if0(self, image, state):
        condits = dict(zip(
            '==,!=,<,>,<=,>='.split(','),
            '!=,==,>=,<=,>,<'.split(',')))

        def expr(block):
            new_block = copy.copy(block)
            new_block.children = list()
            state = 0
            prev = None

            for expr in block.children:
                if state == 0:
                    if isinstance(expr, AssignExpr) and isinstance(expr.expr, BinaryExpr):
                        if expr.expr.op in condits:
                            prev = expr
                            state = 1
                            continue
                    elif isinstance(expr, (OpAssignExpr)) and (expr.var, expr.op) == ('ip', '+') and isinstance(expr.expr, VarExpr):
                        prev = expr
                        state = 3
                        continue
                    new_block.append(expr)

                elif state == 1:
                    if isinstance(expr, (OpAssignExpr)) and (expr.var, expr.op) == ('ip', '+') and isinstance(expr.expr, VarExpr):
                        if expr.expr.var == prev.var:
                            state = 2
                            continue
                    new_block.append(prev)
                    new_block.append(expr)
                    state = 0

                elif state == 2:
                    cond = prev.expr
                    icond = BinaryExpr(cond.expr1, condits[cond.op], cond.expr2)
                    if_expr = IfExpr(icond, expr)
                    if_expr.source = prev.source
                    if_expr.label = prev.label
                    new_block.append(if_expr)
                    state = 0

                elif state == 3:
                    icond = PrefixUnaryExpr('!', prev.expr)
                    if_expr = IfExpr(icond, expr)
                    if_expr.source = prev.source
                    if_expr.label = prev.label
                    new_block.append(if_expr)
                    state = 0

            return new_block

        tr = BlockTransform(expr)
        return state._accept(tr)

    def _if_reduce(self, image, state):
        prev = None
        while state != prev:
            prev = state
            state = self._else_if(image, state)
            state = self._do_while(image, state)
        return state

    def _else_if(self, image, state):
        condits = dict(zip(
            '==,!=,<,>,<=,>='.split(','),
            '!=,==,>=,<=,>,<'.split(',')))

        def expr(block):

            def inner(block):
                new_block = copy.copy(block)
                new_block.children = list()
                state = 0
                if_expr = None

                for expr in block.children:
                    if state == 0:
                        if isinstance(expr, IfExpr) and isinstance(expr.if_true, GotoExpr) and expr.if_false is None:
                            cond, goto = expr.cond, expr.if_true

                            if goto.target_line > expr.source_line:
                                target_line = goto.target_line
                                if_expr = copy.copy(expr)
                                icond = BinaryExpr(cond.expr1, condits[cond.op], cond.expr2)
                                if_expr.cond = icond
                                if_expr.if_true = BlockExpr()
                                if_expr.if_false = None
                                state = 1
                                continue

                        new_block.append(expr)

                    elif state == 1:
                        if expr.source_line == target_line:
                            if len(if_expr.if_true.children) == 1:
                                if_expr.if_true = if_expr.if_true.children[0]
                            new_block.append(if_expr)
                            if_expr = None

                            new_block.append(expr)
                            state = 0
                        else:
                            if_expr.if_true.append(expr)

                assert if_expr is None
                return new_block

            prev = None
            while block != prev:
                prev = copy.copy(block)
                block = inner(block)
            return block

        tr = BlockTransform(expr)
        return state._accept(tr)

    def _do_while(self, image, state):

        def has_gotos(block, target):
            class Stats(ExprTraverse):
                def __init__(self):
                    self.labels = set()
                def goto_expr(self, expr):
                    self.labels.add(expr.target)

            stats = Stats()
            block._accept(stats)
            return target in stats.labels

        def expr(block):

            def inner(block):
                for expr in block.children:
                    if isinstance(expr, IfExpr) and isinstance(expr.if_true, GotoExpr) and expr.if_false is None:
                        cond, goto = expr.cond, expr.if_true
                        if block.source_line <= goto.target_line < expr.source_line:
                            break
                else:
                    return block

                start, end = goto.target_line, expr.source_line

                new_block = copy.copy(block)
                new_block.children = list()
                do_while = None
                outside = BlockExpr()

                for expr in block.children:
                    if not do_while:
                        if expr.source_line == start:
                            do_while = DoWhileExpr()
                            do_while.source = expr.source
                            do_while.label = expr.label
                            do_while.expr.append(expr)
                            if has_gotos(outside, expr.label):
                                return block
                        else:
                            new_block.append(expr)
                            outside.append(expr)
                    else:
                        if expr.source_line == end:
                            do_while.cond = expr.cond

                            if has_gotos(do_while.expr, expr.label):
                                blank = BlankExpr()
                                blank.source = expr.source
                                blank.label = expr.label
                                do_while.expr.append(blank)

                            new_block.append(do_while)
                            do_while = None
                        else:
                            do_while.expr.append(expr)
                            if has_gotos(outside, expr.label):
                                return block

                return new_block

            prev = None
            while block != prev:
                prev = copy.copy(block)
                block = inner(block)
            return block

        tr = BlockTransform(expr)
        return state._accept(tr)

    def _at_exit(self, image, state):
        atexit = BlankExpr()
        atexit.label = 'lnexit'

        class Stats(ExprTraverse):
            def __init__(self):
                self.labels = set()
            def goto_expr(self, expr):
                self.labels.add(expr.target)

        stats = Stats()
        state._accept(stats)

        if atexit.label in stats.labels:
            state.append(atexit)

        return state, stats.labels

    def _generate(self, image, state, output=None):
        state, labels = state

        writer = ExprWriter(labels=labels, output=output)
        state._accept(writer)
        return writer.getvalue()


class Expr:
    def __init__(self):
        self.source = None
        self.label = None

    def __eq__(self, other):
        if type(other) is type(self):
            return self.source == other.source
        return False

    @property
    def source_line(self):
        if self.source:
            return self.source.line

    def _accept(self, visitor):
        return visitor.expr(self)


class ExprSource:
    def __init__(self, line, instr=None):
        self.line = line
        self.lines = [(line, instr)]

    def __repr__(self):
        return f'Source({self.line}: {repr(self.lines)})'

    def __eq__(self, other):
        if type(other) is type(self):
            return self.line == other.line
        return False

    def add(self, line, instr=None):
        self.lines.append((line, instr))


class BlankExpr(Expr):
    def _accept(self, visitor):
        return visitor.blank_expr(self)

    def __repr__(self):
        return f'Blank()'

    def __eq__(self, other):
        return super().__eq__(other)


class ConstExpr(Expr):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return f'Const({self.val})'

    def __eq__(self, other):
        if super().__eq__(other):
            return self.val == other.val
        return False

    def _accept(self, visitor):
        return visitor.const_expr(self)


class VarExpr(Expr):
    def __init__(self, var):
        super().__init__()
        self.var = var

    def __str__(self):
        return self.var

    def __repr__(self):
        return f'Var({self.var})'

    def __eq__(self, other):
        if super().__eq__(other):
            return self.var == other.var
        return False

    def _accept(self, visitor):
        return visitor.var_expr(self)


class BlockExpr(Expr):
    def __init__(self, children=None):
        super().__init__()
        self.children = list()
        if children:
            for child in children:
                self.append(child)

    def __repr__(self):
        return f'Block({", ".join(map(repr, self.children))})'

    def __eq__(self, other):
        if super().__eq__(other):
            return self.children == other.children
        return False

    def append(self, expr):
        self.children.append(expr)
        if not self.source:
            self.source = expr.source
        if not self.label:
            self.label = expr.label

    def _accept(self, visitor):
        return visitor.block_expr(self)


class AssignExpr(Expr):
    def __init__(self, var, expr):
        super().__init__()
        self.var = var
        self.expr = expr

    def __repr__(self):
        return f'Assign({self.var} = {repr(self.expr)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.var == other.var) and (self.expr == other.expr)
        return False

    def _accept(self, visitor):
        return visitor.assign_expr(self)


class OpAssignExpr(Expr):
    def __init__(self, var, op, expr):
        super().__init__()
        self.var = var
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'OpAssign({self.var} {self.op}= {repr(self.expr)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.var == other.var) and (self.op == other.op) and (self.expr == other.expr)
        return False

    def _accept(self, visitor):
        return visitor.opassign_expr(self)


class BinaryExpr(Expr):
    def __init__(self, expr1, op, expr2):
        super().__init__()
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2

    def __repr__(self):
        return f'Binary({repr(self.expr1)} {self.op} {repr(self.expr2)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.expr1 == other.expr1) and (self.op == other.op) and (self.expr2 == other.expr2)
        return False

    def _accept(self, visitor):
        return visitor.binary_expr(self)


class PrefixUnaryExpr(Expr):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'PrefixUnary({self.op} {repr(self.expr)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.op == other.op) and (self.expr == other.expr)
        return False

    def _accept(self, visitor):
        return visitor.prefix_unary_expr(self)


class GotoExpr(Expr):
    def __init__(self, target_line, target):
        super().__init__()
        self.target_line = target_line
        self.target = target

    def __repr__(self):
        return f'Goto({self.target})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.target_line == other.target_line)
        return False

    def _accept(self, visitor):
        return visitor.goto_expr(self)


class IfExpr(Expr):
    def __init__(self, cond, if_true, if_false=None):
        super().__init__()
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false

    def __repr__(self):
        return f'If({repr(self.cond)}, true: {repr(self.if_true)}, false: {repr(self.if_false)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.cond == other.cond) and (self.if_true == other.if_true) and (self.if_false == other.if_false)
        return False

    def _accept(self, visitor):
        return visitor.if_expr(self)


class DoWhileExpr(Expr):
    def __init__(self, cond=None, expr=None):
        super().__init__()
        self.cond = cond
        self.expr = expr or BlockExpr()

    def __repr__(self):
        return f'DoWhile({repr(self.cond)}, {repr(self.expr)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.cond == other.cond) and (self.expr == other.expr)
        return False

    def _accept(self, visitor):
        return visitor.do_while_expr(self)


class ForLoopExpr(Expr):
    def __init__(self, cond=None, expr=None):
        super().__init__()
        self.init = None
        self.cond = cond
        self.step = None
        self.expr = expr or BlockExpr()

    def __repr__(self):
        return f'ForLoop(init: {repr(self.init)}, while: {repr(self.cond)}, step: {repr(self.step)}, do: {repr(self.expr)})'

    def __eq__(self, other):
        if super().__eq__(other):
            return (self.cond == other.cond) and (self.init == other.init) and (self.step == other.step) and (self.expr == other.expr)
        return False

    def _accept(self, visitor):
        return visitor.for_loop_expr(self)


class ExprWriter:
    def __init__(self, labels=None, output=None):
        self.labels = labels or set()
        self.so = output or io.StringIO()
        self._indent = 0
        self.newline = True
        self.tab = '    '
        self.no_semi = False

    def getvalue(self):
        if hasattr(self.so, 'getvalue'):
            return self.so.getvalue()

    def indent(self, x=1):
        self._indent += x

    def unindent(self, x=1):
        self._indent -= x

    def _write_indent(self):
        if self.newline:
            self.so.write(self.tab * self._indent)

    def write(self, text):
        self._write_indent()
        self.so.write(text)
        self.newline = text and text[-1] == '\n'

    def write_line(self, text=''):
        self._write_indent()
        self.so.write(text)
        self.so.write('\n')
        self.newline = True

    def expr_source(self, source):
        for ln, instr in source.lines:
            self.write(f'// line {ln}:')
            if instr:
                op, a, b, c = instr
                self.write(f' {op} {a} {b} {c}')
            self.write_line()

    def expr(self, expr):
        if expr.label and expr.label in self.labels:
            # if expr.source:
            #     self.expr_source(expr.source)
            self.so.write(f'{expr.label}:\n')

    def blank_expr(self, expr):
        self.expr(expr)
        # self.write_line()

    def const_expr(self, expr):
        self.write(str(expr.val))

    def var_expr(self, expr):
        self.write(expr.var)

    def block_expr(self, expr):
        for child in expr.children:
            child._accept(self)

    def assign_expr(self, expr):
        self.expr(expr)
        self.write(expr.var)
        self.write(' = ')
        expr.expr._accept(self)
        if not self.no_semi:
            self.write_line(';')

    def opassign_expr(self, expr):
        self.expr(expr)
        self.write(expr.var)
        self.write(f' {expr.op}= ')
        expr.expr._accept(self)
        if not self.no_semi:
            self.write_line(';')

    def binary_expr(self, expr):
        expr.expr1._accept(self)
        self.write(f' {expr.op} ')
        expr.expr2._accept(self)

    def prefix_unary_expr(self, expr):
        self.write(f'{expr.op}')
        expr.expr._accept(self)

    def goto_expr(self, expr):
        self.expr(expr)
        self.write_line(f'goto {expr.target};')

    def if_expr(self, expr):
        self.expr(expr)
        self.write('if (')
        expr.cond._accept(self)
        self.write_line(') {')
        self.indent()
        expr.if_true._accept(self)
        self.unindent()
        self.write('}')
        if expr.if_false:
            self.write_line(' else {')
            self.indent()
            expr.if_false._accept(self)
            self.unindent()
            self.write('}')
        self.write_line()

    def do_while_expr(self, expr):
        self.expr(expr)
        self.write_line('do {')
        self.indent()
        expr.expr._accept(self)
        self.unindent()
        self.write('} while (')
        expr.cond._accept(self)
        self.write_line(');')

    def for_loop_expr(self, expr):
        self.expr(expr)
        self.no_semi = True
        self.write('for (')
        if expr.init:
            expr.init._accept(self)
        self.write('; ')
        expr.cond._accept(self)
        self.write(';')
        if expr.step:
            self.write(' ')
            expr.step._accept(self)
        self.write_line(') {')
        self.no_semi = False
        self.indent()
        expr.expr._accept(self)
        self.unindent()
        self.write_line('}')


class ExprTraverse:
    def blank_expr(self, expr):
        return expr

    def const_expr(self, expr):
        return expr

    def var_expr(self, expr):
        return expr

    def block_expr(self, expr):
        for child in expr.children:
            child._accept(self)
        return expr

    def assign_expr(self, expr):
        expr.expr._accept(self)
        return expr

    def opassign_expr(self, expr):
        expr.expr._accept(self)
        return expr

    def binary_expr(self, expr):
        expr.expr1._accept(self)
        expr.expr2._accept(self)
        return expr

    def prefix_unary_expr(self, expr):
        expr.expr._accept(self)
        return expr

    def goto_expr(self, expr):
        return expr

    def if_expr(self, expr):
        expr.cond._accept(self)
        expr.if_true._accept(self)
        if expr.if_false:
            expr.if_false._accept(self)
        return expr

    def do_while_expr(self, expr):
        expr.expr._accept(self)
        expr.cond._accept(self)
        return expr

    def for_loop_expr(self, expr):
        if expr.init:
            expr.init._accept(self)
        expr.cond._accept(self)
        if expr.step:
            expr.step._accept(self)
        expr.expr._accept(self)
        return expr


class ExprTransform(ExprTraverse):
    def block_expr(self, expr):
        res = copy.copy(expr)
        res.children = [x._accept(self) for x in expr.children]
        return res

    def assign_expr(self, expr):
        res = copy.copy(expr)
        res.expr = expr.expr._accept(self)
        return res

    def opassign_expr(self, expr):
        res = copy.copy(expr)
        res.expr = expr.expr._accept(self)
        return res

    def binary_expr(self, expr):
        res = copy.copy(expr)
        res.expr1 = expr.expr1._accept(self)
        res.expr2 = expr.expr2._accept(self)
        return res

    def prefix_unary_expr(self, expr):
        res = copy.copy(expr)
        res.expr = expr.expr._accept(self)
        return res

    def if_expr(self, expr):
        res = copy.copy(expr)
        res.cond = expr.cond._accept(self)
        res.if_true = expr.if_true._accept(self)
        if expr.if_false:
            res.if_false = expr.if_false._accept(self)
        return res

    def do_while_expr(self, expr):
        res = copy.copy(expr)
        res.cond = expr.cond._accept(self)
        res.expr = expr.expr._accept(self)
        return res

    def for_loop_expr(self, expr):
        res = copy.copy(expr)
        if expr.init:
            res.init = expr.init._accept(self)
        res.cond = expr.cond._accept(self)
        if expr.step:
            res.step = expr.step._accept(self)
        res.expr = expr.expr._accept(self)
        return res


class BlockTransform(ExprTransform):
    def __init__(self, tr):
        self.tr = tr

    def block_expr(self, expr):
        res = super().block_expr(expr)
        return self.tr(res)
