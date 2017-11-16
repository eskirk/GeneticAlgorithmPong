import random


class Synapse:
    def __init__(self, start_neuron, end_neuron, weight=0):
        if weight == 0:
            self.randomize()
        else:
            self.weight = weight
        self.start_neuron = start_neuron
        self.end_neuron = end_neuron

    def __str__(self):
        return str(self.start_neuron) + '----' + '{0:.2}'.format(self.weight) + '--->' + str(self.end_neuron)

    def __repr__(self):
        return str(self.weight)

    def randomize(self):
        self.weight = random.uniform(-1, 1)

    def set_weight(self, weight):
        self.weight = weight

