from enum import Enum

class Color(Enum):
    """
    In french and lowercase for convenience when getting data from tiles
    """
    rose = 1
    bleu = 2
    rouge = 3
    gris = 4
    marron = 5
    noir = 6
    violet = 7
    blanc = 8

class Suspect(Enum):
    SUSPECT = 1
    CLEAN = 2

class Tile:
    def __init__(self, color: Color, pos, suspect: Suspect):
        self._color = color
        self._pos = pos
        self._suspect = suspect

    def __str__(self):
        return '{0}/{1}/{2}'.format(self._color, self._pos, self._suspect)
