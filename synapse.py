import random


class Synapse:
    def __init__(self, weight, start_neuron, end_neuron):
        self.weight = weight
        self.start_neuron = start_neuron
        self.end_neuron = end_neuron

    def randomize(self):
        self.weight = random.uniform(0, 1)
