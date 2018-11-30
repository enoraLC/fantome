import sys
from world import World
from time import sleep

#Start
if len(sys.argv) == 2:
    sleep(2)
    w = World(int(sys.argv[1]))
    w.play()
