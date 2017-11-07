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
        self.population_size = population_size

    def start_breeding(self):
        self.create_new_population()
        population = []

        for game in self.games:
            # play the game using this neural net and record the fitness function
            game.start_game()
            while not game.game_over:
                pass
            population.append(game.paddle1)

        population = sorted(population, key=lambda x: x.fitness, reverse=True)
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
            ai_1 = NNPaddle(PongGame.window_width / 2, PongGame.window_height / 2, ball, game)
            ai_2 = NNPaddle(50, PongGame.window_height / 2, ball, game)

            population.append(ai_1)
            population.append(ai_2)
            self.games.append(game)

        self.population = population

    def breed_best(self, population):
        best, next_best = population[:2]

        print(best, next_best)
        for p in population[::-1]:
            p.save_genome()

        # neural net sex

        # return super child

        # return best  # need to actually do the sex part

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
        print(offspring.net.synapses)

        for layer in range(len(offspring.net.synapses)):
            for synapse in range(len(offspring.net.synapses[layer])):
                if random.uniform(0, 1) > 0.5:
                    print('parent1')
                    offspring.net.synapses[layer][synapse].weight = parent1.net.synapses[layer][synapse].weight
                else:
                    print('parent2')
                    offspring.net.synapses[layer][synapse].weight = parent2.net.synapses[layer][synapse].weight
            print()
        print(offspring.net.synapses)
        f_name = random.choice(parent1.name.split())
        l_name = random.choice(parent2.name.split())
        offspring.name = f_name + ' ' + l_name

        print(offspring.name)

    def randomize(self):
        pass

    def mutate(self):
        pass


def main():
    if len(sys.argv) > 1:
        breeder = NeuralNetBreeder(int(sys.argv[1]))
    else:
        breeder = NeuralNetBreeder(10)
    pop = breeder.start_breeding()
    breeder.breed_best(pop)
    breeder.crossover(pop[0], pop[1])


if __name__ == '__main__':
    main()







