from enum import Enum
from time import sleep

class Fopera_file:
    latency = 0.01

    def __init__(self, path):
        self._path = path
        self._last_question = ''
        self._f = None

    def read_until_data(self):
        with open(self._path, 'r') as f:
            s = f.readline()

        #No data or same question (== no new question)
        while not s or s == self._last_question:
            with open(self._path, 'r') as f:
                sleep(self.latency)
                s = f.readline()
        self._last_question = s
        return s

    def write(self, msg):
        f = open(self._path, 'w')
        f.write(msg)
        f.close()

    def continuous_read(self):
        if self._f is None:
            self._f = open(self._path, 'r', encoding="ISO-8859-1")
        s = self._f.readline()

        while (not s):
            sleep(self.latency)
            s = self._f.readline()
        return s
