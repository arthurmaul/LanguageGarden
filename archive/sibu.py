#!/usr/bin/python

import tui
from os import system as shell
from sys import argv as args
from copy import copy
from tui import Setting, code, style

prompt = style(Setting.BRIGHT_WHITE, Setting.BOLD)
response = code(Setting.BOLD)
divider = style(Setting.YELLOW, Setting.BOLD)
failure = style(Setting.RED, Setting.BOLD)
success = style(Setting.GREEN, Setting.BOLD)
number = style(Setting.CYAN)

class Sibu:
    def __init__(self):
        self.lexicon = default_lexicon()
        self.context = list()
        self.running = True
        self.done = False
        self.failed = False
        self.line = 1
        self.position = 1
        self.cursor = 0

    def reload(self):
        Sibu.__init__(self, self.source)

    def fail(self, message, lexeme):
        print(failure(message))
        print("ln: ", self.line, "pos:", self.position - len(lexeme))
        self.failed = True

    def comment(self):
        while self.source[self.cursor] != ")":
            self.read()
        self.read()

    def inspect(self):
        if (lexeme := self.read()) == "EOF": return self.fail("There is nothing to inspect.")
        match lexeme:
            case "Lexicon": found = (lexeme for lexeme in self.lexicon)
            case "Core": found = (l for l, d in self.lexicon.items() if callable(d))
            case "Defined": found = (l for l, d in self.lexicon.items() if not callable(d))
            case _:
                if lexeme in self.lexicon:
                    if callable(lexicon[lexeme]): return print(f"builtin({lexeme})")
                    print(lexeme, " ".join(self.lexicon[lexeme]))
                else: self.fail(f"{lexeme}?", lexeme)

    def define(self):
        definition = list()
        lexeme = self.read()
        while (next := self.read()) != ";":
            if self.done:
                return self.fail("You never finished your definition!", lexeme)
            definition.append(next)
        self.lexicon[lexeme] = " ".join(definition)
        return self.read()

    def doloop(self):
        repeats = self.context.pop()
        body = list()
        while (lexeme := self.read()) != "loop":
            body.append(lexeme)
        self.read()
        for _ in range(repeats):
            for lexeme in body:
                self.interpret(lexeme)

    def text(self):
        string = list()
        while (lexeme := self.read()) != "\"":
            string.append(lexeme)
        self.context.append(" ".join(str(word) for word in string))

    def show_text(self):
        self.text()
        print(self.context.pop())

    def needs(self):
        self.load(self.read())

    def retrieve(self, lexeme):
        definition = self.lexicon[lexeme]
        if callable(definition):
            return definition(self)
        for l in definition:
            self.interpret(l)

    def read(self):
        lexeme = list()
        while not self.done:
            if self.cursor == len(self.source):
                self.done = True
                if lexeme: return "".join(lexeme)
                return "EOF"
            next = self.source[self.cursor]
            self.cursor += 1
            if next == "\n":
                self.line += 1
                self.position = 0
                if lexeme: return "".join(lexeme)
            elif next == " ":
                self.position += 1
                if lexeme: return "".join(lexeme)
            else:
                self.position += 1
                lexeme.append(next)

    def interpret(self, lexeme):
        match lexeme:
            case "(":
                # print("comment detected")
                return self.comment()
            case "see":
                # print("see directive detected")
                return self.inspect()
            case ":":
                # print("compile directive detected")
                return self.define()
            case "do":
                # print("do directive detected")
                return self.doloop()
            case "\"":
                # print("text directive detected")
                return self.text()
            case ".\"":
                # print("comment detected")
                return self.show_text()
            case "'":
                # print("comment detected")
                return self.rune()
            case ".'":
                # print("comment detected")
                return self.show_rune()
            case "needs":
                # print("needs directive detected")
                return self.needs()
            case "reload":
                # print("reload directive detected")
                return self.reload()
            case lexeme if lexeme in self.lexicon:
                # print("lexeme detected")
                return self.retrieve(lexeme)
            case lexeme if lexeme.isdigit():
                # print("digit detected")
                return self.context.append(int(lexeme))
            case unknown:
                # print("unknown detected")
                return self.fail(f"{unknown}?", unknown)

    def run(self):
        while not self.done:
            program = self.read()
            if program:
                self.interpret(program)

    def load(self, path):
        with open(f"{path}.psa") as source:
            self.source = source.read()
        self.run()

    def dialog(self):
        self.source = ""
        while self.running:
            program = tui.read(f"{prompt('\u03A3(')}{number(len(self.context))}{prompt(')')} {divider('::')} {response}")
            self.source += "\n" + program if self.source else program
            self.run()
            self.done = False
            if not self.failed:
                print(success("Ok"))
            else:
                self.failed = False
                self.line -= 1

    def start(self):
        match args:
            case [_, path]: self.load(path)
            case [_]: self.dialog()
            case _: print("no")

def add(app):
    c = app.context
    c.append(c.pop() + c.pop())

def sub(app):
    c = app.context
    y, x = c.pop(), c.pop()
    c.append(x - y)

def mul(app):
    c = app.context
    c.append(c.pop() * c.pop())

def div(app):
    c = app.context
    c.append(c.pop() / c.pop())

def mod(app):
    c = app.context
    c.append(c.pop() % c.pop())

def gt(app):
    c = app.context
    c.append(1 if c.pop() < c.pop() else 0)

def lt(app):
    c = app.context
    c.append(1 if c.pop() > c.pop() else 0)

def nor(app):
    c = app.context
    c.append(1 if c.pop() == 0 and c.pop() == 0 else 0)

def dup(app):
    c = app.context
    c.append(copy(c[-1]))

def drop(app):
    c = app.context
    c.pop()

def emit(app):
    c = app.context
    print(chr(c.pop()), end="")

def peek(app):
    c = app.context
    print("Context : ", end="")
    print(f"({number(" ".join(str(element) for element in c))})")

def pop(app):
    c = app.context
    print(number(c.pop()))
    
def echoed(app):
    c = app.context
    "echoed  Takes a value and prints it to the screen"
    print(c[-1])

def leave(app):
    app.running = False

def default_lexicon():
    return {
        "+": add, "-": sub, "*": mul, "/": div, "%": mod, ">": gt, "<": lt, "nor": nor,
        "?": peek, ".": pop, "echoed": echoed, "emit": emit, "bye": leave,
        "dup": dup, "drop": drop, "cls": lambda c: shell("clear")
    }

if __name__ == "__main__":
    sibu = Sibu()
    sibu.start()

