from enum import Enum
from spell import Spell, Spell_type

class Question_type(Enum):
    UNKNOWN = 0
    TILE = 1
    POSITION = 2
    SPELL_ACTIVATION = 3
    SPELL = 4

class Question:
    def __init__(self, q):
        self._question = q
        self._type = self.get_question_type(q)
        if self._type == Question_type.UNKNOWN:
            self._spell = Spell(self._question)
            self._type = Question_type.SPELL if self._spell._type != Spell_type.UNKNOWN else Question_type.UNKNOWN

    def __str__(self):
        return '{0}: {1}'.format(self._type, self._question)

    @staticmethod
    def get_question_type(s):
        if 'Tuiles' in s:
            return Question_type.TILE
        elif 'positions' in s and '-' not in s:
            return Question_type.POSITION
        elif 'pouvoir' in s:
            return Question_type.SPELL_ACTIVATION
        return Question_type.UNKNOWN
