#!/bin/sh

python ./client.py 1 > phantom.log &
python ./client.py 0 > inspector.log &
python ./fantome_opera_serveur.py && echo 'END OF GAME: FANTOME_OPERA' &&
  killall python
