from enum import Enum

from typer.colors import RED, BLACK, GREEN, BRIGHT_RED


class Level(Enum):
    d = 0
    i = 1
    w = 2
    e = 3

    def color(self):
        # return self.value
        match self.value:
            case 0:
                return BLACK
            case 1:
                return GREEN
            case 2:
                return BRIGHT_RED
            case 2:
                return RED


class Log(object):
    def __init__(self, time="", process="", origin="", translated="", level: Level = Level.d, type=""):
        self.time = time
        self.process = process
        self.origin = origin
        self.translated = translated
        self.level = level
        self.type = type

    def __str__(self):
        return self.time + " | " + self.process + " | " + self.translated
        # return self.time + ">" + self.process + ">" + self.origin_msg + ">" + self.translated_msg


if __name__ == '__main__':
    print(Level.d.value)
    print(Level.d.name)
