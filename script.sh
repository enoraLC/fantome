#!/bin/sh

python3 ./client.py 1 > phantom.log &
python3 ./client.py 0 > inspector.log &
python3 ./fantome_opera_serveur.py  && echo 'END OF GAME: FANTOME_OPERA' && tail -n 1 0/infos.txt &&
  killall python3
