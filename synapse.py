import random


class Synapse:
    def __init__(self, start_neuron, end_neuron, weight=None):
        if weight is None:
            self.randomize()
        else:
            self.weight = weight
        self.start_neuron = start_neuron
        self.end_neuron = end_neuron

    def __str__(self):
        return str(self.start_neuron) + '----' + '{0:.2}'.format(self.weight) + '--->' + str(self.end_neuron)

    def randomize(self):
        self.weight = random.uniform(0, 1)

