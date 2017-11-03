import random


class Neuron:
    def __init__(self):
        self.value = None

    def randomize(self):
        self.value = random.uniform(0, 1)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_value(self, value):
        self.value += value
