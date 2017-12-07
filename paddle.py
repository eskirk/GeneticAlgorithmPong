import pygame
import math
import random

from neural_net import NeuralNet


class Paddle:
    def __init__(self, x_pos, y_pos):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.score = 0
        self.fitness = 0
        self.contacts_ball = 0
        self.name = 'Player'

    def draw(self, display):
        pygame.draw.rect(display, (0, 0, 255), self.bounds)

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def reset(self, x_pos, y_pos, ball):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)

    def follow_ball(self, delta):
        pass


class AIPaddle(object):
    def __init__(self, x_pos, y_pos, ball, game):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.ball = ball
        self.game = game
        self.score = 0
        self.fitness = 0
        self.contacts_ball = 0
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
        elif (self.ball.bounds.y + self.ball.bounds.width) < (self.bounds.y + self.bounds.height) and self.bounds.y > 0:
            self.move_up(delta)

    def reset(self, x_pos, y_pos, ball):
        self.ball = ball
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)


class NNPaddle(object):
    def __init__(self, x_pos, y_pos, ball, game, four_player=False):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)
        self.ball = ball
        self.game = game
        self.four_player = four_player
        # self.net = NeuralNet(4, 1, 3)
        self.net = NeuralNet(3, 1, 3)
        self.generation = 0
        self.score = 0
        self.fitness = 0
        self.contacts_ball = 0
        self.name = self.random_name()
        self.parents = []

        self.colors = None
        self.color_ndx = 0
        self.seizure_reduction = 0
        self.seize_rate = random.uniform(0, 15)
        self.set_colors()

    def __repr__(self):
        return str(self.name) + ' score: ' + str(self.score) + ' contacts: ' + str(self.contacts_ball) + \
            ' gen: ' + str(self.generation)

    def __gt__(self, other):
        return self.fitness > other.fitness

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
        color_1 = (random.uniform(0, 255), random.uniform(
            0, 255), random.uniform(0, 255))
        color_2 = (random.uniform(0, 255), random.uniform(
            0, 255), random.uniform(0, 255))
        color_3 = (random.uniform(0, 255), random.uniform(
            0, 255), random.uniform(0, 255))
        color_4 = (random.uniform(0, 255), random.uniform(
            0, 255), random.uniform(0, 255))
        self.colors = [color_1, color_2, color_3, color_4]
        self.color_ndx = 0
        self.color_ndx = int(random.uniform(0, 4))

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def follow_ball(self, delta):
        y_pos = self.bounds.y + self.bounds.height
        ball_y = self.ball.bounds.y
        ball_speed = math.sqrt(self.ball.vel_x**2 + self.ball.vel_y**2)

        inputs = [y_pos, ball_y, ball_speed]
        output = self.net.get_output(inputs)
        if not self.four_player:
            if output > 0.5:
                if self.bounds.y + self.bounds.height < self.game.window_height:
                    self.move_down(delta)
            else:
                if self.bounds.y > 0:
                    self.move_up(delta)
        else:
            if output > 0.5:
                if self.bounds.y + self.bounds.height < self.game.window_height - 50:
                    self.move_down(delta)
            else:
                if self.bounds.y > 50:
                    self.move_up(delta)

    def reset(self, x_pos, y_pos, ball):
        self.ball = ball
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)

    def save_genome(self, file_path='./genomes/'):
        path = file_path + str(self.name)
        f = open(path, 'w+')

        for synapse in self.net.synapses:
            f.write(str(synapse) + '\n')
        f.write(self.name + '\n')
        f.write(str(self.generation) + '\n')
        f.close()

    def load_genomes(self, file):
        try:
            f = open('./final_genomes/' + file)
        except FileNotFoundError:
            try:
                f = open('./genomes/' + file)
            except FileNotFoundError:
                print(FileNotFoundError)
                return
        layer_number = 0
        synapses = []
        name, gen = False, False

        for line in f:
            if len(line) > 0 and line[0] == '[' and layer_number <= self.net.num_hidden_layers:
                gene = []
                synapse = line.split(',')
                for s in synapse:
                    if '[' in s:
                        gene.append(float(s.strip('[')))
                    elif '\n' in s:
                        gene.append(float(s.strip(']\n')))
                    else:
                        gene.append(float(s))
                synapses.append(gene)
                layer_number += 1
            elif not name:
                self.name = line.strip('\n')
                name = True
            elif not gen:
                self.generation = int(line.strip('\n'))
                gen = True

        for i in range(len(self.net.synapses)):
            for j in range(len(self.net.synapses[i])):
                self.net.synapses[i][j].weight = synapses[i][j]

        print('Loaded genome:', self)

    @staticmethod
    def random_name():
        names = ['Cheenis', 'Garreth', 'Baxter', 'Slidey', 'McPong', 'Jeeves', 'Jacob', 'Bool', 'Don', 'Cheedle', 'Don',
                 'Cheedle', 'Stanley', 'Alexa', 'The Pacer Test', 'Finn', 'Daniel', 'Dan the Man', 'Dad', 'The Alamo',
                 'Grobgobbler', 'Gavin', 'Doyle', '@RealGavin', 'Juul', 'Bruul', 'Dr.', 'Bichael', 'Flats', 'Andrew',
                 'Farquaad', 'Blanch', 'Son of', 'Dreyfuss', 'Chad', 'Donald', 'Chump', 'Too Many', 'Bocephus',
                 'Diengklurg', 'Antwaun', 'Dart', 'Joe', 'Szymczyk', 'Stratton', 'Go', 'Bears', 'Jabarbwire', 'Barbara',
                 'Bush', 'Dante', 'Soldavini', 'Rick']
        if random.uniform(0, 1) > 0.5:
            return random.choice(names)
        else:
            temp_names = list(names)
            f_name = random.choice(temp_names)
            temp_names.remove(f_name)
            l_name = random.choice(temp_names)
            return f_name + ' ' + l_name


class SidewaysNNPaddle(NNPaddle):
    def __init__(self, x_pos, y_pos, ball, game):
        NNPaddle.__init__(self, x_pos, y_pos, ball, game)
        self.bounds = pygame.Rect(x_pos, y_pos, 100, 15)

    def follow_ball(self, delta):
        x_pos = self.bounds.x + self.bounds.width
        ball_x = self.ball.bounds.x
        ball_speed = math.sqrt(self.ball.vel_x**2 + self.ball.vel_y**2)

        inputs = [x_pos, ball_x, ball_speed]
        output = self.net.get_output(inputs)
        if output > 0.5:
            if self.bounds.x + self.bounds.width < self.game.window_width - 50:
                self.move_left(delta)
        else:
            if self.bounds.x > 50:
                self.move_right(delta)

    def move_right(self, delta):
        self.bounds = self.bounds.move(-250 * delta, 0)

    def move_left(self, delta):
        self.bounds = self.bounds.move(250 * delta, 0)

    def reset(self, x_pos, y_pos, ball):
        self.ball = ball
        self.bounds = pygame.Rect(x_pos, y_pos, 100, 15)