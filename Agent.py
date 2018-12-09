import random
from NeuralNetwork import NeuralNetwork


class Agent(object):
    def __init__(self, name="Roger", actions=[], neural_network=None):
        self.name = name
        self.fitness = None
        self.history = None
        self.died = False
        self.actions = actions
        # Set a random neural network if none is provided
        self.neural_network = NeuralNetwork("IA-{}".format(name))

        # self.neural_network.add_input("hp")
        # self.neural_network.add_input("apples")
        for action in actions:
            self.neural_network.add_output(action)
        #     self.neural_network.connect("hp", action)
        #     self.neural_network.connect("apples", action)

        # At this point, we have a fully random neural network between hp and apples
        # And the actions given in the ctor.
        # self.neural_network.dump()


    # Returns action and actions with probabilities
    def think(self, environment):
        actions = self.neural_network.think(environment)
        action = None
        max = 100
        highest_value = -1
        for choice in actions:
            if choice[1] > highest_value:
                highest_value = choice[1]
                action = choice[0]
            # i = random.random() * max
            # if i < choice[1]:
            #     action = choice[0]
            #     break
            # else:
            #     max -= choice[1]
        return action, actions

    def setNeuralNetwork(self, neural_network):
        self.neural_network = neural_network