# Projet: Fantome

## Intelligence Artificielle

Nous avons developpé un réseau de neurone simple que nous avons ensuite optimisé par algorithme évolutionniste.
Cette partie est celle sur laquelle nous nous sommes concentrés, car elle était nécessaire pour la suite du développement.

Vous trouverez le code relatif à l'IA dans Agent.py, NeuralNetwork.py et Training.py.
Agent.py decrit une classe permettant facilement de créer des agents intelligents et de les utiliser (avec la méthode think)
Training.py est un terrain d'entrainement dans lequel un mini jeu (ou l'agent doit gagner un maximum de points) est codé, et on les individus sont entrainés par génération (algorithme évolutioniste).
NeuralNetwork.py code à partir de zéro un réseau de neurone simple mais fonctionnel.

Pour tester la phase d'entrainement, vous pouvez charger le script Training.py dans un interpreteur Python et executer la méthode train_gen:

```def train_gen(nbGens=15, nbAgents=15, nbPlays=10)```

## Jeu

Malheureusement, n'ayant pas eu le temps de mettre au service du jeu en lui même notre travail d'IA, le modèle n'est pas vraiment compatible avec le jeu. Si les inputs sont cohérents selon nous, les outputs ne sont pas vraiment adaptés aux questions posées par le serveur. 
Le modèle est le suivant : Le reseau de neurone observe le tour de jeu, la position des joueurs et si il est le fantome.
En fonction de cela, il repond 0, 1, 2 ou 3.

Inputs   ----------------  Outputs
[Tour]                     [0]
[Shadow]                   [1]
[is_fantom]                [2]
[rose]                     [3]
[bleu]
[rouge]
[gris]
[marron]
[noir]
[violet]
[blanc]

