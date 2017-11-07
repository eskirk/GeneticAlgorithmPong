import pygame
import math
import random

from neuron import Neuron
from synapse import Synapse


class NeuralNet:
    def __init__(self, num_inputs, num_hidden_layers, num_neurons):
        self.fitness = None
        self.output = Neuron()
        self.inputs = [Neuron() for _ in range(num_inputs)]
        self.hidden_layers = [[Neuron() for _ in range(num_neurons)] for _ in range(num_hidden_layers)]
        self.synapses = [[] for _ in range(num_hidden_layers + 1)]
        self.num_hidden_layers = num_hidden_layers
        self.init_synapses()

    def init_synapses(self):
        # link inputs and first hidden layer
        for input_ndx, input_neuron in enumerate(self.inputs):
            for neuron in self.hidden_layers[0]:
                self.synapses[0].append(Synapse(input_neuron, neuron))

        # link hidden layers to each other
        if len(self.hidden_layers) > 1:
            for curr_ndx in range(len(self.hidden_layers) - 1):
                for neuron in self.hidden_layers[curr_ndx]:
                    for next_neuron in self.hidden_layers[curr_ndx + 1]:
                        self.synapses[curr_ndx + 1].append(Synapse(neuron, next_neuron))

        # link last layer to output
        for neuron in self.hidden_layers[len(self.hidden_layers) - 1]:
            self.synapses[len(self.synapses) - 1].append(Synapse(neuron, self.output))

    def get_output(self, inputs):
        # set the value of the input neurons to the input values passed in
        for inp in enumerate(inputs):
            self.inputs[inp[0]].set_value(inp[1])

        # go through each of the synapses and add the values to the next layer of neurons
        for i in range(self.num_hidden_layers):
            for synapse in self.synapses[i]:
                synapse.end_neuron.add_value(synapse.weight * synapse.start_neuron.get_value())
            # once all the values have been added together, apply the sigmoid to the final value of the neuron
            for neuron in self.hidden_layers[i]:
                neuron.set_value(NeuralNet.sigmoid(neuron.get_value()))

        # generate the final value by adding all the final layers values together
        for synapse in self.synapses[self.num_hidden_layers]:
            synapse.end_neuron.add_value(synapse.weight * synapse.start_neuron.get_value())

        # apply the sigmoid function to the final neuron's value
        self.output.set_value(NeuralNet.sigmoid(self.output.get_value()))
        # print(self.output, ' final layer, post sigmoid')

        return self.output.get_value()

    @staticmethod
    def sigmoid(x):
        if x > 700:
            x = 700
        elif x < -700:
            x = -700
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            print(x, ' overflow')
            x = -x
            return 1 / (1 + math.exp(x))


class AIPaddle:
    def __init__(self, x_pos, y_pos, ball, game):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.ball = ball
        self.game = game
        self.score = 0
        self.fitness = 0
        self.name = 'AIPaddle'

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

    def reset(self, x_pos, y_pos, ball):
        self.ball = ball
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)


class NNPaddle:
    def __init__(self, x_pos, y_pos, ball, game):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.ball = ball
        self.game = game
        self.net = NeuralNet(4, 1, 3)
        self.generation = 0
        self.score = 0
        self.fitness = 0
        self.name = self.random_name()

        self.colors = None
        self.color_ndx = 0
        self.seizure_reduction = 0
        self.seize_rate = random.uniform(0, 15)

    def __repr__(self):
        return str(self.name) + ' : ' + str(self.fitness)

    def draw(self, display):
        random.seed()
        if self.colors is None:
            color_1 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            color_2 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            color_3 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            color_4 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            self.colors = [color_1, color_2, color_3, color_4]
            self.color_ndx = 0
            self.color_ndx = int(random.uniform(0, 4))
        self.seizure_reduction += 1
        if self.seizure_reduction > self.seize_rate:
            self.color_ndx = int(random.uniform(0, 4))
            self.seizure_reduction = 0

        pygame.draw.rect(display, (self.colors[self.color_ndx]), self.bounds)

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def follow_ball(self, delta):
        y_pos = self.bounds.y + self.bounds.height
        ball_y = self.ball.bounds.y
        ball_vel_x = self.ball.vel_x
        ball_vel_y = self.ball.vel_y
        inputs = [y_pos, ball_y, ball_vel_x, ball_vel_y]

        # print(inputs, ' inputs')
        output = self.net.get_output(inputs)
        if output > 0.5:
            if self.bounds.y + self.bounds.height < self.game.window_height:
                self.move_down(delta)
        else:
            if self.bounds.y > 0:
                self.move_up(delta)

    def reset(self, x_pos, y_pos, ball):
        self.ball = ball
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)

    def save_genome(self):
        path = './genomes/' + str(self.name)
        f = open(path, 'w+')

        for synapse in self.net.synapses:
            f.write(str(synapse))

    @staticmethod
    def random_name():
        names = ['Cheenis', 'Garreth', 'Baxter', 'Slidey', 'McPong', 'Slidey McPong', 'Jeeves', 'Jacob', 'Bool',
                 'Don Cheenal', 'Don', 'Cheenal', 'Stanley', 'Alexa', 'The Pacer Test', 'Finn', 'Daniel', 'Dan the Man',
                 'Dad', 'The Alamo', 'Grobgobbler', 'Gavin', 'Doyle', '@RealGavin']
        if random.uniform(0, 1) > 0.5:
            return random.choice(names)
        else:
            temp_names = list(names)
            f_name = random.choice(temp_names)
            temp_names.remove(f_name)
            l_name = random.choice(temp_names)
            return f_name + ' ' + l_name


if __name__ == '__main__':
    net = NeuralNet(4, 1, 3)
    inps = [0, 0, 0, 0]
    print('Inputs: ', inps)
    print('Output:', net.get_output(inps))


