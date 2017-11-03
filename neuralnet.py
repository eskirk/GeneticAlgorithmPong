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
        self.hidden_layers = [[Neuron() for _ in range(num_neurons)] for _ in range(num_hidden_layers)]
        self.synapses = [[] for _ in range(num_hidden_layers + 1)]
        self.num_hidden_layers = num_hidden_layers
        self.init_synapses()

        for synapse_layer in self.synapses:
            for synapse in synapse_layer:
                print(synapse)
            print()

    def init_synapses(self):
        # link inputs and first hidden layer
        for input_ndx, input_neuron in enumerate(self.inputs):
            for neuron in self.hidden_layers[0]:
                self.synapses[0].append(Synapse(input_neuron, neuron))

        # link rest of hidden layers

        # link last layer to output
        for neuron in self.hidden_layers[len(self.hidden_layers) - 1]:
            self.synapses[len(self.synapses) - 1].append(Synapse(neuron, self.output))

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
            for neuron in self.hidden_layers[i]:
                neuron.set_value(self.sigmoid(neuron.get_value()))

        # generate the final value by adding all the final layers values together
        for synapse in self.synapses[self.num_hidden_layers]:
            synapse.end_neuron.add_value(synapse.start_neuron.get_value())

        # apply the sigmoid function to the final neuron's value
        self.output.set_value(self.sigmoid(self.hidden_layers[self.num_hidden_layers][0]))

        return self.output.get_value()

    def init_output(self):
        self.output = Neuron()

    # sort the genomes and cross them over with all other genomes
    def crossover(self):
        pass

    def set_neuron_values(self):
        pass

    def sigmoid(self, x):
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

