import random


class Neuron:
    def __init__(self, value):
        self.value = value

    def randomize(self):
        self.value = random.uniform(0, 1)
