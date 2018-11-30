import sys
from world import World
from time import sleep
from fopera_file import Fopera_file

#Start
if len(sys.argv) == 2:
    # This line avoid to fetch questions from old game launched
    sleep(Fopera_file.latency)
    w = World(int(sys.argv[1]))
    w.play()
