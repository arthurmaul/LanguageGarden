import sys
from enum import IntEnum, auto

# Style combinators? ie instead of a parser, its a painter

class Setting(IntEnum):
    # General styling.
    BOLD          = 1
    FAINT         = 2
    ITALIC        = 3
    UNDERLINE     = 4
    INVERSE       = 7
    STRIKETHROUGH = 9

    # The 8 standard colors.
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37

    # The bright variants
    BRIGHT_BLACK   = 60 + 30
    BRIGHT_RED     = 60 + 31
    BRIGHT_GREEN   = 60 + 32
    BRIGHT_YELLOW  = 60 + 33
    BRIGHT_BLUE    = 60 + 34
    BRIGHT_MAGENTA = 60 + 35
    BRIGHT_CYAN    = 60 + 36
    BRIGHT_WHITE   = 60 + 37

    # The background variants
    BLACK_BACKGROUND   = 30 + 10
    RED_BACKGROUND     = 31 + 10
    GREEN_BACKGROUND   = 32 + 10
    YELLOW_BACKGROUND  = 33 + 10
    BLUE_BACKGROUND    = 34 + 10
    MAGENTA_BACKGROUND = 35 + 10
    CYAN_BACKGROUND    = 36 + 10
    WHITE_BACKGROUND   = 37 + 10

    # The bright background variants
    BRIGHT_BLACK_BACKGROUND   = 60 + 30 + 10
    BRIGHT_RED_BACKGROUND     = 60 + 31 + 10
    BRIGHT_GREEN_BACKGROUND   = 60 + 32 + 10
    BRIGHT_YELLOW_BACKGROUND  = 60 + 33 + 10
    BRIGHT_BLUE_BACKGROUND    = 60 + 34 + 10
    BRIGHT_MAGENTA_BACKGROUND = 60 + 35 + 10
    BRIGHT_CYAN_BACKGROUND    = 60 + 36 + 10
    BRIGHT_WHITE_BACKGROUND   = 60 + 37 + 10

    # All the options set to their default.
    RESET = 0

def style(*settings):
    def wrap(text):
        return f"{code(*settings)}{text}{code(Setting.RESET)}"
    return wrap

def code(*settings):
    return f"\x1b[{";".join(map(str, (setting.value for setting in settings)))}m"

def enable(*settings):
    print(code(settings), end="") 

def normalize():
    """Sets all of the options to the default set by the terminal."""
    print(code(Setting.RESET), end="")

def read(prompt):
    response = input(prompt)
    normalize()
    return response

class Text:
    def __init__(self):
        self.data = list()
        self.length = 0

    def render(self):
        ...

class Canvas:
    def __init__(self):
        self.data = list()
        self.width = 0
        self.height = 0

    def render(self):
        ...

class LayeredCanvas:
    def __init__(self):
        self.data = list()
        self.width = 0
        self.height = 0
        self.depth = 0

    def render(self):
        ...

