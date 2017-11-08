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

    def start_breeding(self):
        self.create_new_population()
        population = []

        for game in self.games:
            # play the game using this neural net and record the fitness function
            game.paddle1.ball = game.ball
            game.paddle2.ball = game.ball

            game.start_game()
            population.append(game.paddle1)
            print(game.paddle1)

        population = sorted(population, key=lambda x: x.fitness)
        for individual in population:
            print(individual)

        return population

    def create_new_population(self, starting_network=None):
        population = []
        temp_population_size = self.population_size
        if starting_network:
            population.extend(starting_network)
            temp_population_size -= 1

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
        offspring = copy.deepcopy(parent1)
        offspring.fitness = 0
        offspring.generation = self.generation
        # print(offspring.net.synapses)

        for layer in range(len(offspring.net.synapses)):
            for synapse in range(len(offspring.net.synapses[layer])):
                if random.uniform(0, parent1.fitness + parent2.fitness) > parent2.fitness:
                    # print('parent1')
                    offspring.net.synapses[layer][synapse].weight = parent1.net.synapses[layer][synapse].weight
                else:
                    # print('parent2')
                    offspring.net.synapses[layer][synapse].weight = parent2.net.synapses[layer][synapse].weight
            offspring.colors = [parent1.colors[0], parent2.colors[1], parent1.colors[2], parent2.colors[3]]
            print()
        f_name = random.choice(parent1.name.split())
        l_name = random.choice(parent2.name.split())
        offspring.name = f_name + ' ' + l_name

        return offspring

    def randomize(self):
        pass

    def mutate(self):
        pass

    def evolve(self, pop):
        self.generation += 1
        population = list(sorted(pop, key=lambda x: x.fitness))
        print('GENERATION: ', self.generation)
        for p in population:
            print(p)
        children = []
        while len(population) > 1:
            parent1 = population.pop()
            parent2 = population.pop()
            offspring = self.crossover(parent1, parent2)
            offspring.generation = self.generation

            game = PongGame()
            offspring.ball = game.ball
            game.paddle1 = offspring
            game.start_game()

            print('parents: ', parent1, parent2)
            print(offspring)
            offspring.save_genome()
            children.append(offspring)
        if len(population) == 1:
            children.append(population[0])
        return children


def main():
    if len(sys.argv) > 1:
        breeder = NeuralNetBreeder(int(sys.argv[1]))
    else:
        breeder = NeuralNetBreeder(10)
    population = breeder.start_breeding()

    while len(population) > 1:
        population = breeder.evolve(population)


if __name__ == '__main__':
    main()







