import random


class Neuron:
    def __init__(self, value=None):
        if value is None:
            self.randomize()
        else:
            self.value = value

    def randomize(self):
        self.value = random.uniform(0, 1)
