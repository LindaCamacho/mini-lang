# interpreter.py
import sys
from antlr4 import *
from .MiniLangLexer import MiniLangLexer
from .MiniLangParser import MiniLangParser
from .MiniLangVisitor import MiniLangVisitor

class EvalVisitor(MiniLangVisitor):
    def __init__(self):
        super().__init__()
        self.memory = {}

    def visitProgram(self, ctx:MiniLangParser.ProgramContext ):
        for st in ctx.statement():
            self.visit(st)
        return None

    def visitStatement(self, ctx:MiniLangParser.StatementContext):
        if ctx.assign():
            return self.visit(ctx.assign())
        if ctx.print_():
            return self.visit(ctx.print_())
        if ctx.expr():
            value = self.visit(ctx.expr())
            print(value)
            return value
        return None

    def visitAssign(self, ctx:MiniLangParser.AssignContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[var_name] = value
        return value

    # print : 'print' '(' expr ')' ;
    def visitPrint(self, ctx:MiniLangParser.PrintContext):
        value = self.visit(ctx.expr())
        print(value)
        return value

    def visitExpr(self, ctx:MiniLangParser.ExprContext):
        if ctx.INT():
            return int(ctx.INT().getText())

        if ctx.ID():
            name = ctx.ID().getText()
            if name not in self.memory:
                raise NameError(f"Variable '{name}' no definida")
            return self.memory[name]

        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expr(0))

        op = getattr(ctx, 'op', None)
        if op is not None:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            sym = op.text
            if sym == '*':
                return left * right
            elif sym == '/':
                if right == 0:
                    raise ZeroDivisionError("División por cero")
                return left / right
            elif sym == '+':
                return left + right
            elif sym == '-':
                return left - right

        # No reconocido
        raise Exception("Expresión no reconocida: " + ctx.getText())

def evaluate_source(source: str, visitor: EvalVisitor):
    input_stream = InputStream(source)
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    tree = parser.program()
    return visitor.visit(tree)

def run_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    visitor = EvalVisitor()
    evaluate_source(src, visitor)

def repl():
    visitor = EvalVisitor()
    print("MiniLang. Escribe una instrucción: ")
    try:
        while True:
            try:
                line = input('>>> ')
            except EOFError:
                break
            if line.strip() == "":
                continue
            try:
                evaluate_source(line + "\n", visitor)
            except Exception as e:
                print("Error:", e)
    except KeyboardInterrupt:
        print("\nSaliendo...")
    return

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        repl()
