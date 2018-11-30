import sys
import re
from fopera_file import Fopera_file
from tile import Tile, Color
from question import Question, Question_type

class World():
    def __init__(self, player_id):
        # Keep player id. Needed to find the player folder
        self._player_id = player_id;
        # For debug
        self._player_type = "inspector" if self._player_id == 0 else "phantom";
        # One object Fopera_file for each file that are used to communicate with
        # the server
        self._question_file = Fopera_file('{base}/questions.txt'.format(base=player_id))
        self._infos_file = Fopera_file('{base}/infos.txt'.format(base=player_id))
        self._response_file = Fopera_file('{base}/reponses.txt'.format(base=player_id))
        # List of questions fetched from the file 'questions.txt'
        self._questions = []

    def retrieve_info(self):
        # Player 1 is the phantom.
        # It may need to know which character is the phantom
        if self._player_id == 1:
            l = self._infos_file.continuous_read()
            self._phantom_color = Color[l[l.index(':') + 2:-1]]
        # Fetch world state
        self._infos_file.continuous_read()
        line = self._infos_file.continuous_read()
        r = re.search(r'^Tour:(?P<tour>[0-9]*),'
                      '.*Score:(?P<score_v>[0-9]*)/(?P<score_m>[0-9]*),'
                      '.*Ombre:(?P<shadow>[0-9]*),'
                      '.*Bloque:{(?P<bloque>.*)}$', line)
        self._tour = int(r.group('tour'))
        self._score = r.group('score_v')
        self._max_score = r.group('score_m')
        self._shadow = int(r.group('shadow'))
        self._block = [int(x) for x in r.group('bloque').split(',')]
        line = self._infos_file.continuous_read()
        self._tiles = []
        for data in [tile.strip().split('-') for tile in line.split()]:
            self._tiles.append(Tile(data[0], data[1], data[2]))

    def play(self):
        self.retrieve_info()
        while (True):
            self.read_question()
            self.answer_question()
            sys.stdout.flush()

    def read_question(self):
        line = self._question_file.read_until_data()
        q = Question(line)
        if q._type is not Question_type.UNKNOWN:
            self._questions.append(q)
            print("Question for {1}: {0}".format(Question(line), self._player_type))

    def answer_question(self):
        if len(self._questions) > 0:
            response = ''
            q = self._questions.pop()
            if q._type is Question_type.TILE:
                for t in self.choose_tile(q._question):
                    print(t)
                response = '3'
            elif q._type is Question_type.POSITION:
                for p in self.choose_position(q._question):
                    print(p)
                response = '2'
            elif q._type is Question_type.SPELL_ACTIVATION:
                response = '1'
            elif q._type is Question_type.SPELL:
                for data in q._spell.get_spell_data():
                    print(data)
                response = '0'
            else:
                print('KO: {0}'.format(q))
                return
            self._response_file.write(response)
            print("{0} answer: {1}".format(self._player_type, response))

    @staticmethod
    def choose_tile(q):
        tiles = []
        for data in [tile.strip().split('-') for tile in q[q.index('[') +
            1:q.index(']')].split(',')]:
            tiles.append(Tile(data[0], data[1], data[2]))
        return tiles

    @staticmethod
    def choose_position(q):
        return [int(x) for x in q[q.index('{') + 1:q.index('}')].split(',')]

    @property
    def player_id(self):
        '''
        Player id
        '''
        return self.player_id

    @property
    def tour(self):
        '''
        Tour number of the game
        '''
        return self._tour

    @property
    def score(self):
        '''
        Current score evaluated by the server
        '''
        return self._score

    @property
    def max_score(self):
        '''
        Max score evaluated by the server
        '''
        return self._max_score

    @property
    def shadow(self):
        '''
        Data about the room shadowed (everybody in the room are considered
        alone)
        '''
        return self._shadow

    @property
    def block(self):
        '''
        Data about the path blocked
        '''
        return self._block

    @property
    def tiles(self):
        '''
        Data about the tiles
        '''
        return self._tiles
