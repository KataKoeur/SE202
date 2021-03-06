from ast.nodes import *
from utils.visitor import *


class Dumper(Visitor):

    def __init__(self, semantics):
        """Initialize a new Dumper visitor. If semantics is True,
        additional information will be printed along with declarations
        and identifiers."""
        self.semantics = semantics

    @visitor(None)
    def visit(self, node):
        raise Exception("unable to dump %s" % node)

    @visitor(IntegerLiteral)
    def visit(self, i):
        return str(i.intValue)

    @visitor(BinaryOperator)
    def visit(self, binop):
        # Always use parentheses to reflect grouping and associativity,
        # even if they may be superfluous.
        return "(%s %s %s)" % \
               (binop.left.accept(self), binop.op, binop.right.accept(self))

    @visitor(Assignment)
    def visit(self, a):
        return "%s := %s" % (a.identifier.accept(self), a.exp.accept(self))

    @visitor(IfThenElse)
    def visit(self, c):
        if c.else_part is None:
            return "if %s then %s" % \
                    (c.condition.accept(self), c.then_part.accept(self))
        else:
            return "if %s then %s else %s" % \
                    (c.condition.accept(self), c.then_part.accept(self), c.else_part.accept(self))

    @visitor(Let)
    def visit(self, let):
        d = ""
        e = ""
        for decl in let.decls:
            d += decl.accept(self) + ' '
        for exp in let.exps:
            e += exp.accept(self) + '; '
        e = e[:-2] + ' ' if e else ""
        return "let %sin %send" % (d, e)

    @visitor(Type)
    def visit(self, type):
        return "%s" % (type.typename)

    @visitor(VarDecl)
    def visit(self, var):
        scope = '/*e*/' if self.semantics and var.escapes else ''
        if var.type == None:
            return "var %s := %s" % (var.name+scope, var.exp.accept(self))
        elif var.exp == None:
            return "%s: %s" % (var.name+scope, var.type.accept(self))
        else:
            return "var %s: %s := %s" % (var.name+scope, var.type.accept(self), var.exp.accept(self))

    @visitor(FunDecl)
    def visit(self, fun):
        a = ""
        for arg in fun.args:
            a += arg.accept(self) + ', '
        a = a[:-2]
        if fun.type == None or fun.type.typename == 'void':
            return "function %s(%s) = %s" % \
                (fun.name, a, fun.exp.accept(self))
        else:
            return "function %s(%s): %s = %s" % \
                (fun.name, a, fun.type.accept(self), fun.exp.accept(self))

    @visitor(FunCall)
    def visit(self, fun):
        p = ""
        for param in fun.params:
            p += param.accept(self) + ', '
        p = p[:-2]
        return "%s(%s)" % (fun.identifier.accept(self), p)

    @visitor(SeqExp)
    def visit(self, sq):
        e = ""
        for exp in sq.exps:
            e += exp.accept(self) + '; '
        e = e[:-2]
        if len(sq.exps) == 1:
            return "%s" % (e)
        else:
            return "(%s)" % (e)

    @visitor(While)
    def visit(self, w):
        return "while %s do %s" % (w.condition.accept(self), w.exp.accept(self))

    @visitor(For)
    def visit(self, f):
        return "for %s := %s to %s do %s" % \
        (f.indexdecl.accept(self), f.low_bound.accept(self), f.high_bound.accept(self), f.exp.accept(self))

    @visitor(IndexDecl)
    def visit(self, i):
        return "%s" % (i.name)

    @visitor(Break)
    def visit(self, b):
        return "break"

    @visitor(Identifier)
    def visit(self, id):
        if self.semantics and type(id.decl) is VarDecl:
            diff = id.depth - id.decl.depth
            scope_diff = "/*%d*/" % diff if diff else ''
        else:
            scope_diff = ''
        return '%s%s' % (id.name, scope_diff)
