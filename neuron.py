import random


class Neuron:
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return '{0:.10f}'.format(self.value)

    def randomize(self):
        self.value = random.uniform(0, 1)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_value(self, value):
        self.value += value
