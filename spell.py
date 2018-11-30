from enum import Enum
from tile import Color

class Spell_type(Enum):
    GREY = 0
    BLUE_ROOM = 1
    BLUE_PATH = 2
    VIOLET = 3
    WHITE = 4
    UNKNOWN = 5

class Spell:
    def __init__(self, q):
        self._question = q
        self._type = self.get_spell_type(q)

    def __str__(self):
        return '{0}:{1}'.format(self._type, self._question)

    @staticmethod
    def get_spell_type(q):
        if 'obscurcir' in q:
            return Spell_type.GREY
        elif 'bloquer' in q:
            return Spell_type.BLUE_ROOM
        elif 'sortie' in q:
            return Spell_type.BLUE_PATH
        elif 'échanger' in q:
            return Spell_type.VIOLET
        elif 'position' in q:
            return Spell_type.WHITE
        return Spell_type.UNKNOWN

    def get_spell_data(self):
        print("Active spell used: {0}".format(self._type))
        if self._type == Spell_type.GREY or self._type == Spell_type.BLUE_ROOM:
            """ Quelle salle obscurcir ? (0-9) """
            """ Quelle salle bloquer ? (0-9) """
            return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        elif self._type == Spell_type.BLUE_PATH:
            """ Quelle sortie ? Chosir parmi : {0, 2} """
            q = self._question
            return [int(x) for x in q[q.index('{') + 1:q.index('}')].split(',')]
        elif self._type == Spell_type.VIOLET:
            """ Avec quelle couleur échanger (pas violet!) ?  """
            return [Color.rose, Color.bleu, Color.rouge, Color.gris,
                    Color.marron, Color.noir, Color.blanc]
        elif self._type == Spell_type.WHITE:
            """ rose-6-suspect, positions disponibles : {5, 7}, choisir la valeur """
            q = self._question
            return [int(x) for x in q[q.index('{') + 1:q.index('}')].split(',')]
        return []
