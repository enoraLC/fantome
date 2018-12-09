#
# Training and testing for Agent class
#
import os
import random
import sys
from functools import reduce
import time
from Agent import Agent
from NeuralNetwork import train, NeuralNetwork

def load_nn(path, name="Agent"):
    fd = open(path)
    lines = fd.readlines()

    ag = Agent("{} 00{}".format(name, i), ['eat', 'fight'])
    nn = NeuralNetwork("nn")
    inputs = {}

    # TODO: Make generic in connect if output_name not known
    nn.add_output("eat")
    # nn.add_output("nothing")
    nn.add_output("fight")
    for line in lines:
        if line[0] == '#':
            continue
        splitWithEqual = line.split('=')
        link = splitWithEqual[0].split('-')
        weight = splitWithEqual[1].split('+')[0]
        bias = splitWithEqual[1].split('+')[1]
        if link[0] in inputs.keys():
            inputs[link[0]][link[1]] = float(weight)
        else:
            inputs[link[0]] = {}
            inputs[link[0]][link[1]] = float(weight)
        for key, value in inputs.items():
            nn.add_input(key)
            for output, weight in value.items():
                nn.connect(key, output, [weight, bias])

    ag.setNeuralNetwork(nn)
    nn.dump()
    fd.close()
    return ag

def play(agent):

    history = []
    # User score (how many turns the user stays alive, if the player eats two apples in a row, he loses 5 points)
    score = 0

    # Some values the agent can use as inputs
    environment = {
        'hp': 100,
        'apples': 10,
        'fights': 0,
        # 'nothing': 0,
        'done': False,
    }

    while environment['apples'] > 0 and environment['hp'] > 0:
        score += 1
        # Returns the action the agent takes, but also the vector of actions the agent could have taken with probabilities.
        action, actions = agent.think(environment)
        if action is not None:
            history += [action]
            if action == "eat":
                # Remove an apple
                environment['apples'] -= 1
                # Give back some hp
                environment['hp'] += 10

                # Useless eating
                if environment['hp'] > 100:
                    environment['hp'] = 100
                    score +=1
                else:
                    # Normal eating
                    score += 45

            if action == "fight":
                environment['fights'] += 1
                environment['hp'] -= 25
                if environment['hp'] <= 0:
                    score -= 1000
                else:
                    score += 50

        if action == "nothing" or action is None:
            environment['nothing'] += 1
            environment['hp'] -= 2
            score -= 5
    if environment['hp'] <= 0:
        agent.died = True
        print("Player is dead")
    nb_times = {
        'eat': 0,
        'fight': 0,
        'nothing': 0,
    }
    for h in history:
        nb_times[h] += 1
    agent.fitness = score
    agent.history = history
    # The game is over, we return the agent's score.
    return {
        'agent': agent,
        'score': score,
        'history': history,
    }

# Now that we have an agent, we'll let it "play" a number of times and see its scores.
def game(name, generation, nbPlays):

    scores = []
    agts = []
    for agent in generation:
        avgScore = 0
        for _ in range(nbPlays):
            res = play(agent)
            avgScore += res['score']
        scores += [avgScore / nbPlays]
        agts += [res['agent']]
    return scores, agts

best = {}
def trainAgain(index, agents, file, nbAgents, nbPlays):
    best['score'] = 0
    best['agent'] = None

    generation = game("First game", agents, nbPlays)

    average = reduce(lambda x, y: x + y, generation[0]) / len(generation[0])
    file.write("Current average fitness is : {}\n".format(average))
    nextGenAgents = []
    next = []
    trained = 0
    for i in range(nbAgents):
        if agents[i].fitness > best['score']:
            best['score'] = agents[i].fitness
            best['agent'] = agents[i]
        nbr = random.random() * 100
        next += [Agent("Agent 00{}".format(i), ['eat', 'fight'])]
        if nbr > 15:
            nextGenAI = train(generation[1], "NextGen-{}".format(i))
            next[-1].setNeuralNetwork(nextGenAI)
            trained += 1
    file.write("Next gen has {} new agents, and {} are trained\n".format(nbAgents - trained, trained))
    return next

def train_gen(nbGens=15, nbAgents=15, nbPlays=10):
    agents = []
    for i in range(nbAgents):
        agents += [Agent("Agent 00{}".format(i), ['eat', 'fight'])]

    file = open("trace", "w")
    saved_nn = open("saved_nn", "w")

    i = 0
    while i < nbGens or False:
        agents = trainAgain(i, agents, file, nbAgents, nbPlays)

        agents[0].neural_network.dump()
        i += 1
    if best['agent'] is None:
        print("NO BEST AGENT")
    try:
        file.write("Final AI best score and NN is : \n")
        file.write("Score: {}\n".format(best['score']))
        file.write("NN: {}\n".format(best['agent'].neural_network.dump(True)))
        saved_nn.write('# Scored: {}\n'.format(best['score']))
        saved_nn.write(best['agent'].neural_network.dump(True))
    except Exception as e:
        print("An error occured while printing to file: {}".format(e))
    file.close()
    saved_nn.close()
    return best['agent']