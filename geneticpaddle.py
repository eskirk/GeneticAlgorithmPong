import pygame
import math
import random

from neuron import Neuron
from synapse import Synapse
from pong import PongGame


class GeneticPaddle:
    def __init__(self, x_pos, y_pos, ball, game):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.ball = ball
        self.fitness = 0
        self.game = game
        self.generation = 0
        self.genes = []
        self.name = self.random_name()
        self.score = 0

        self.colors = None
        self.color_ndx = 0
        self.seizure_reduction = 0
        self.seize_rate = random.uniform(0, 15)

    def __repr__(self):
        return str(self.name) + ' fitness: ' + str(self.fitness) + ' gen: ' + str(self.generation)

    def draw(self, display):
        random.seed()
        if self.colors is None:
            self.set_colors()
        self.seizure_reduction += 1
        if self.seizure_reduction > self.seize_rate:
            self.color_ndx = int(random.uniform(0, 4))
            self.seizure_reduction = 0

        pygame.draw.rect(display, (self.colors[self.color_ndx]), self.bounds)

    def set_colors(self):
        color_1 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        color_2 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        color_3 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        color_4 = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.colors = [color_1, color_2, color_3, color_4]
        self.color_ndx = 0
        self.color_ndx = int(random.uniform(0, 4))

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def follow_ball(self, delta):
        pass

    def determine_action(self):
        position = self.ball.get_position()
        # determine which sector the ball is and look in the genes to see the corresponding action
        sector = self.find_sector(position)
        # return the action corresponding to the position of the ball
        return self.genes[sector[0]][sector[1]]

    def find_sector(self, position):

        return (x_sector, y_sector)

    def reset(self, x_pos, y_pos, ball):
        self.ball = ball
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)

    def save_genome(self):
        path = './genomes/' + str(self.name)
        f = open(path, 'w+')

        for synapse in self.genes:
            f.write(str(synapse) + '\n')
        f.write(self.name + '\n')
        f.write(str(self.generation) + '\n')
        f.write(str(self.colors))
        f.close()

    def load_genomes(self, file):
        f = open(file)

        # for line in f:

    @staticmethod
    def random_name():
        names = ['Cheenis', 'Garreth', 'Baxter', 'Slidey', 'McPong', 'Slidey McPong', 'Jeeves', 'Jacob', 'Bool',
                 'Don Cheedle', 'Don', 'Cheedle', 'Stanley', 'Alexa', 'The Pacer Test', 'Finn', 'Daniel', 'Dan the Man',
                 'Dad', 'The Alamo', 'Grobgobbler', 'Gavin', 'Doyle', '@RealGavin', 'Juul', 'Bruul', 'Dr.', 'Bichael',
                 'Flats', 'Andrew', 'Farquaad', 'Blanch', 'Son of', 'Dreyfuss', 'Chad', 'Donald', 'Chump', 'Too Many',
                 'Bocephus', 'Diengklurg', 'Antwaun', 'Dart']
        if random.uniform(0, 1) > 0.5:
            return random.choice(names)
        else:
            temp_names = list(names)
            f_name = random.choice(temp_names)
            temp_names.remove(f_name)
            l_name = random.choice(temp_names)
            return f_name + ' ' + l_name


if __name__ == '__main__':

