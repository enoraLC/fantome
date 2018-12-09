from numpy import exp, array, random, dot, tanh
import random


def sigmoid(x):
    return 1 / (1+exp(x))

# Takes an object with an array of scores and an array of neural networks
def train(generation, suffix="1"):
    if len(generation) < 3:
        print("Generation is too small !")
        return generation
    # Sort the agents by fitness and take the best 2 and the worst
    generation.sort(key=lambda x: x.fitness, reverse=True)
    print("Sorted: {}".format(generation))
    for agent in generation:
        print(agent.fitness)
    nextGenAI = NeuralNetwork("NextGen-{}".format(suffix))
    for input in generation[0].neural_network.inputs:
        nextGenAI.add_input(input['name'], input['bias'])
    for action in generation[0].neural_network.outputs:
        nextGenAI.add_output(action)

        def averagelinks(agents, inputname, outputname):
            weights = []
            biases = []
            index = -1
            for agent in agents:
                index += 1
                actual_input = None
                for input in agent.neural_network.inputs:
                    if input['name'] == inputname:
                        actual_input = input
                        break
                biases += [actual_input['bias']]
                actual_weight = None
                for link, weight in actual_input['links'].items():
                    if link == outputname:
                        actual_weight = weight
                        break
                weights += [actual_weight]
            final_weight = sum(weights) / len(agents)
            final_bias = sum(biases) / len(agents)
            return final_weight, final_bias

        for input in generation[0].neural_network.inputs:
            average_input_weight = averagelinks([generation[0], generation[1], generation[0]], input['name'], action)
            nextGenAI.connect(input['name'], action, average_input_weight)
    return nextGenAI


class NeuralNetwork(object):
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

    def activation_function(self, neuron_value):
        return sigmoid(neuron_value)

    def normalize(self, array):
        values = [p[1] for p in array]
        next = []
        total = sum(values)
        index = 0
        for pair in array:
            next += [(pair[0], (values[index] / total) * 100)]
            index += 1
        return next

    # Returns an array of tuple ("name", proba (0-100))
    def think(self, inputs):
        result = []
        if len(self.outputs) == 0:
            raise Exception("No outputs in neural network.")
        for output in self.outputs:
            value = 0
            for input in self.inputs:
                for link, weight in input['links'].items():
                    if link == output:
                        input_value = inputs[input['name']]
                        value += weight * input_value
            result += [(output, self.activation_function(value))]
        return self.normalize(result)

    def add_input(self, name, bias=0):
        if bias is None:
            bias = random.random() * 10 - 5
        self.inputs += [{
            'name': name,
            'bias': bias,
            'links': {},
        }]

    def add_output(self, name):
        self.outputs += [name]

    def connect(self, input_name, output_name, weight=None):
        actual_weight = None
        if weight is None:
            actual_weight = random.random() * 10 - 5
        else:
            actual_weight = weight[0]
            self.set_input_bias(input_name, weight[1])
        actual_input = None
        for i in self.inputs:
            if i['name'] == input_name:
                actual_input = i
                break
        actual_input['links'][output_name] = actual_weight

    def set_input_bias(self, input_name, bias=0):
        actual_input = None
        for i in self.inputs:
            if i['name'] == input_name:
                actual_input = i
                break
        actual_input['bias'] = bias

    def dump(self, returnAsString=False):
        if returnAsString:
            str = ""
            for input in self.inputs:
                for link, weight in input['links'].items():
                    str += "{}-{}={}+{}\n".format(input['name'], link, weight, input['bias'])
            return str
        for input in self.inputs:
            for link, weight in input['links'].items():
                print("{}-{}={}+{}".format(input['name'], link, weight, input['bias']))