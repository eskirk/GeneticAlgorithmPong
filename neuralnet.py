class NeuralNet:
    def __init__(self):
        self.fitness = -1

    def __gt__(self, other):
        return self.fitness > other.fitness

    def randomize(self):
        pass

    def mutate(self):
        pass
