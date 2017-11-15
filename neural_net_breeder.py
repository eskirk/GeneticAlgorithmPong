from neuralnet import NeuralNet, AIPaddle, NNPaddle
from pong import PongGame
from ball import Ball
import sys
import copy
import random


class NeuralNetBreeder:
    def __init__(self, population_size):
        self.population = []
        self.games = []
        self.generation = 0
        self.best = []
        self.population_size = population_size
        self.cur_speed = 1000

    def start_breeding(self):
        self.create_new_population(self.population_size)
        population = []

        for game in self.games:
            # set the game up to play using the new paddles and ball
            game.paddle1.ball = game.ball
            game.paddle2.ball = game.ball
            game.speed = self.cur_speed

            # play the game and record the game speed multiplier to use for future games
            game.start_game()
            self.cur_speed = game.speed

            # append the neural net to the population
            population.append(game.paddle1)

        # sort the population best -> worst
        population = sorted(population, key=lambda x: x.fitness)

        return population

    def create_new_population(self, cur_pop_size=0):
        if cur_pop_size > 0:
            population = self.population
        else:
            population = []
        temp_population_size = self.population_size - cur_pop_size

        # create new games and neural net paddles equal to the population size
        for ndx in range(temp_population_size):
            ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
            game = PongGame()
            game.ball = ball
            ai_1 = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, ball, game)
            ai_1.generation = self.generation
            # ai_2 = NNPaddle(50, PongGame.window_height / 2, ball, game)
            game.paddle1 = ai_1

            population.append(ai_1)
            # population.append(ai_2)
            self.games.append(game)

        self.population = population

    # set current genome fit, if all genomes have been set,
    # create a new generation
    def new_genome(self, current_fit):
        pass

    # create a new generation, if the generation has already been initialized,
    # crossover to create a new generation
    def new_generation(self):
        pass

    # sort the genomes and cross them over with all other genomes
    def crossover(self, parent1, parent2):
        # use the parent as a skeleton to create the offspring, like adam and eve or something
        offspring = copy.deepcopy(parent1)
        offspring.fitness = 0
        offspring.generation = self.generation

        # if one parent is significantly more fit than the other, their genes have a higher chance of propagating
        # else if both parent's fitness are equal, the odds of crossover are equal for each of the parents
        if parent1.fitness > parent2.fitness:
            fit = (1/3)
        elif parent2.fitness > parent1.fitness:
            fit = (2/3)
        else:
            fit = 0.5

        # perform crossover for each layer and synapse
        for layer in range(len(offspring.net.synapses)):
            for synapse in range(len(offspring.net.synapses[layer])):
                if random.uniform(0, 1) > fit:
                    offspring.net.synapses[layer][synapse].weight = parent1.net.synapses[layer][synapse].weight
                else:
                    offspring.net.synapses[layer][synapse].weight = parent2.net.synapses[layer][synapse].weight
            # crossover the parent's colors as well
            offspring.colors = [parent1.colors[0], parent2.colors[1], parent1.colors[2], parent2.colors[3]]
            print()
        f_name = random.choice(parent1.name.split())
        l_name = random.choice(parent2.name.split())
        offspring.name = f_name + ' ' + l_name

        return offspring

    def mutate(self):
        pass

    def evolve(self, pop):
        # iterate the generation count
        self.generation += 1
        population = list(sorted(pop, key=lambda x: x.fitness))

        print('\nGENERATION: ', self.generation)
        for p in population:
            if p.fitness > 0:
                print(p)
            else:
                population.remove(p)
        children = []

        if len(population) > 1:
            while len(population) > 1:
                if len(top) == 0:
                    # take the top two parents from the population
                    parent1 = population.pop()
                    parent2 = population.pop()
                    # crossover the top two parents
                    offspring = self.crossover(parent1, parent2)
                    offspring.generation = self.generation
                    print('parents: ', parent1, parent2)
                else:
                    offspring = top.pop()

                # start a new game with the offspring
                game = PongGame()
                game.speed = self.cur_speed
                offspring.ball = game.ball
                offspring.game = game
                game.paddle1 = offspring
                game.start_game()
                self.cur_speed = game.speed

                print(offspring)
                offspring.save_genome()
                children.append(offspring)
        else:
            while len(population) < self.population_size:
                population.append()
        if len(population) == 1:
            children.append(population[0])
        return children


def main():
    if len(sys.argv) > 1:
        breeder = NeuralNetBreeder(int(sys.argv[1]))
    else:
        breeder = NeuralNetBreeder(10)
    self.population = breeder.start_breeding()

    while len(population) > 1:
        population = breeder.evolve(population)


if __name__ == '__main__':
    main()







