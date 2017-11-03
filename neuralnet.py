import pygame
import math
from neuron import Neuron
from synapse import Synapse


class NeuralNet:
    def __init__(self, num_inputs, num_hidden_layers, num_neurons):
        # Copy constructor parameters
        # Create fits array
        # Generate neurons
        # Set biases to 1
        # Generate synapses

        self.fitness = None
        self.output = Neuron()
        self.inputs = [Neuron() for _ in range(num_inputs)]
        self.neurons = [[Neuron() for _ in range(num_neurons)] for _ in range(num_hidden_layers)]
        self.synapses = [[] for _ in range(num_hidden_layers + 1)]
        self.num_hidden_layers = num_hidden_layers
        self.init_synapses()

    def init_synapses(self):
        # link inputs and first hidden layer
        for input_ndx, input_neuron in enumerate(self.inputs):
            for neuron in self.neurons[0]:
                self.synapses[input_ndx].append(Synapse(input_neuron, neuron))

    def init_output(self):
        self.output = Neuron()

    # inputs[0] = ball x position
    # inputs[1] = ball speed
    # inputs[2] = cpu paddle x position
    def get_output(self, inputs):
        # set the value of the input neurons to the input values passed in
        n = 0
        for inp in self.inputs:
            inp.set_value(inputs[n])
            n += 1

        # go through each of the synapses and add the values to the next layer of neurons
        for i in range(self.num_hidden_layers):
            for synapse in self.synapses[i]:
                synapse.end_neuron.add_value(synapse.start_neuron.get_value())
            # once all the values have been added together, apply the sigmoid to the final value of the neuron
            for neuron in self.neurons[i]:
                neuron.set_value(self.sigmoid(neuron.get_value()))

        # generate the final value by adding all the final layers values together
        for synapses in self.synapses[self.num_hidden_layers]:
            for synapse in synapses:
                synapse.end_neuron.add_value(synapse.start_neuron.get_value())

        # apply the sigmoid function to the final neuron's value
        self.output.set_value(NeuralNet.sigmoid(self.output.get_value()))

        return self.output.get_value()

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))


class AIPaddle:
    def __init__(self, x_pos, y_pos, ball, game):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.ball = ball
        self.game = game

    def draw(self, display):
        pygame.draw.rect(display, (0, 0, 255), self.bounds)

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def follow_ball(self, delta):
        if (self.ball.bounds.y + self.ball.bounds.width) > (self.bounds.y + self.bounds.height):
            if self.bounds.y + self.bounds.height < self.game.window_height:
                self.move_down(delta)
        elif (self.ball.bounds.y + self.ball.bounds.width) < (self.bounds.y + self.bounds.height):
            if self.bounds.y > 0:
                self.move_up(delta)


if __name__ == '__main__':
    net = NeuralNet(3, 1, 3)

