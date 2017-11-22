from neuralnet import NeuralNet, AIPaddle, NNPaddle
from pong import PongGame
import copy
import random
import argparse


class NeuralNetBreeder(object):
    def __init__(self, population_size=10, strict_breeding=False, max_generation=5):
        self.population = []
        self.games = []
        self.generation = 0
        self.max_generation = max_generation
        self.best = []
        self.population_size = population_size
        self.cur_speed = 1000
        self.strict_breeding = strict_breeding
        self.train_each_other = False

    def __str__(self):
        return '\n=== Neural Net Breeder ===\nPopulation Size: ' + str(self.population_size) + '\nStrict Breeding: ' + \
               str(self.strict_breeding)

    def init_breeder(self, parent=None):
        # if there is no parent, create a new randomly generated population
        if parent is None:
            self.create_new_population()
            population = []

            for game in self.games:
                # set the game up to play using the new paddles and ball
                game.paddle1.ball = game.ball
                game.paddle2.ball = game.ball
                game.speed = self.cur_speed

                # play the game and record the game speed multiplier to use for future games
                game.start_game()
                print(game.paddle1)
                self.cur_speed = game.speed
                # append the neural net to the population
                population.append(game.paddle1)
            # sort the population best -> worst
            self.population = sorted(population, key=lambda x: x.fitness, reverse=True)
        # if there is a parent, create a generation based off the parent's genes
        elif parent is not None:
            population = [parent]
            self.generation = parent.generation

            game = PongGame()
            parent.game = game
            parent.ball = game.ball
            game.paddle1 = parent

            self.games = [game]
            for i in range(self.population_size - 1):
                population.append(self.crossover(parent))
            self.population = population

    def start_breeding(self):
        # begin creating generations while the generation count is under the desired limit
        while self.generation <= self.max_generation:
            # if the generation is sustainable/fit, start training each other
            if self.generation >= 3:
                self.train_each_other = True
            # if it is the 3rd generation and nobody has scored, create a new generation
            elif self.generation >= 3 and self.best[0].score == 0:
                self.train_each_other = False
                self.population = []

            # play the games and evolve if any of the genomes are successful
            if not self.train_each_other:
                self.play_against_boring_ai()
                best = self.breed()
            # if these genomes are already developed, play against each other
            else:
                self.play_games_against_each_other()
                best = self.breed()

            # if there was a fit genome, save their genome and build a generation off of them
            if best is not None:
                print('\nDaddies of generation', self.generation, ':')
                self.generation += 1
                for genome in best:
                    print(genome)
                best[0].save_genome()
                self.strict_breeding = True
                self.best = list(best)
            if best is None:
                self.train_each_other = False

        # if we reach our desired generation, save the genomes in the ./final_genomes folder
        if self.generation >= self.max_generation:
            print('=== Simulation over ===\n\nResults:')
            for p in self.best:
                print(p)
                p.save_genome('./final_genomes/')

    def create_new_population(self):
        print('\nCreating new population of size', self.population_size)
        self.generation = 0
        self.train_each_other = False
        temp_population_size = self.population_size
        population = []

        # create new games and neural net paddles equal to the population size
        for ndx in range(temp_population_size):
            game = PongGame()
            ai_1 = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, game.ball, game)
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
    def crossover(self, parent1, parent2=None):
        # use the parent as a skeleton to create the offspring, like adam and eve or something
        game = PongGame()
        offspring = copy.deepcopy(parent1)
        offspring.game = game
        offspring.ball = game.ball
        game.paddle1 = offspring
        self.games.append(game)

        # if no other parent, breed with some rando
        if parent2 is None:
            mate = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, offspring.game.ball, offspring.game)
            offspring.parents = [parent1, mate]
        else:
            offspring.parents = [parent1, parent2]
            mate = parent2
        offspring.fitness = 0
        offspring.contacts_ball = 0
        offspring.generation = self.generation

        # perform crossover for each layer and synapse
        for layer in range(len(offspring.net.synapses)):
            for synapse in range(len(offspring.net.synapses[layer])):
                if random.uniform(0, 1) > (1/3):
                    offspring.net.synapses[layer][synapse].weight = parent1.net.synapses[layer][synapse].weight
                else:
                    offspring.net.synapses[layer][synapse].weight = mate.net.synapses[layer][synapse].weight
            # crossover the parent's colors as well
            offspring.colors = [parent1.colors[0], mate.colors[1], parent1.colors[2], mate.colors[3]]
        f_name = random.choice(parent1.name.split())
        l_name = random.choice(mate.name.split())
        offspring.name = f_name + ' ' + l_name

        return offspring

    def mutate(self):
        pass

    def play_against_boring_ai(self):
        # if nobody survived the last generation, generate a new population
        if len(self.population) == 0:
            print('\nCreating new population')
            self.strict_breeding = False
            self.games = []
            self.generation = 0
            while len(self.population) < self.population_size:
                game = PongGame()
                nn_paddle = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, game.ball, game)
                nn_paddle.generation = self.generation
                game.paddle1 = nn_paddle
                # ai_2 = NNPaddle(50, PongGame.window_height / 2, ball, game)
                self.population.append(nn_paddle)
                self.games.append(game)
            for game in self.games:
                game.paddle2.ball = game.ball
                game.speed = self.cur_speed
                game.start_game()
                print(game.paddle1)
                self.cur_speed = game.speed
        else:
            print('\n=== Generation', self.generation, '===')
            for game in self.games:
                game.paddle2.ball = game.ball
                game.paddle2.score = 0
                game.paddle1.score = 0
                game.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, game.ball)
                game.speed = self.cur_speed
                game.start_game()
                print(game.paddle1)
                self.cur_speed = game.speed

    def play_games_against_each_other(self):
        print('\n=== Generation', self.generation, '===')
        # if the number of games is odd, remove the last game in the list
        if len(self.games) % 2 != 0:
            self.games.pop()

        # loop through games two at a time moving the NNPaddle of the second game to the first game
        for game in range(0, len(self.games), 2):
            self.games[game].paddle2 = self.games[game + 1].paddle1

            self.games[game].paddle2.score = 0
            self.games[game].paddle1.score = 0

            self.games[game].paddle2.reset(50, PongGame.window_height / 2, self.games[game].ball)
            self.games[game].paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, self.games[game].ball)

            self.games[game].speed = self.cur_speed
            self.games[game].start_game()
            print('\n', self.games[game].paddle1, '\n\tvs\n', self.games[game].paddle2, '\n')
            self.cur_speed = self.games[game].speed

    def get_fit_individuals(self):
        fit_individuals = []
        for p in self.population:
            if not self.train_each_other:
                if self.strict_breeding and p.fitness > 1 and (p.fitness > p.contacts_ball):
                    print(p)
                    fit_individuals.append(p)
                else:
                    p.fitness += p.contacts_ball
                    if p.fitness > 1:
                        fit_individuals.append(p)
            elif self.train_each_other:
                if p.score == 3 and (p.contacts_ball > p.score):
                    fit_individuals.append(p)

        return fit_individuals

    def breed(self):
        fit_individuals = self.get_fit_individuals()
        self.population = []
        self.games = []

        # if there are fit individuals, use them to create a new population
        if len(fit_individuals) >= 1:
            fit_individuals = sorted(fit_individuals, key=lambda x: x.fitness, reverse=True)
            fittest = fit_individuals[0]

        if len(fit_individuals) == 1:
            while len(self.population) < self.population_size:
                self.population.append(self.crossover(fittest))
        elif len(fit_individuals) > 1:
            second_fittest = fit_individuals[1]
            if not self.strict_breeding:
                fittest = self.crossover(fittest, second_fittest)
                while len(self.population) < self.population_size:
                    self.population.append(self.crossover(fittest))
            else:
                self.population.append(self.crossover(fittest, second_fittest))
                while len(self.population) < self.population_size:
                    temp_population = list(fit_individuals)
                    fittest = random.choice(temp_population)
                    temp_population.remove(fittest)
                    second_fittest = random.choice(temp_population)
                    self.population.append(self.crossover(fittest, second_fittest))

                    while len(self.population) < self.population_size:
                        temp_population = list(fit_individuals)
                        fittest = random.choice(temp_population)
                        temp_population.remove(fittest)
                        second_fittest = random.choice(temp_population)

                        self.population.append(self.crossover(fittest, second_fittest))
            return fit_individuals
        # if there are no fit individuals, return nothing
        return None


def main(args):
    parent = None
    breeder = NeuralNetBreeder(args.p, args.strict, args.g)
    print(breeder)
    if args.load is not None:
        parent = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, None, None)
        parent.load_genomes(args.load)
        breeder.strict_breeding = True

    breeder.init_breeder(parent)
    breeder.start_breeding()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', type=int, default=5)
    parser.add_argument('-p', type=int, default=10)
    parser.add_argument('-load', type=str, default=None)
    parser.add_argument('-strict', type=bool, default=False)
    args = parser.parse_args()

    if args.g <= 0:
        raise argparse.ArgumentTypeError("Minimum generations is 1")

    if args.p <= 1 or args.p % 2 != 0:
        raise argparse.ArgumentTypeError("Minimum population size is 2, population size must be even")

    if args.load is not None and not isinstance(args.load, str):
        raise argparse.ArgumentTypeError("Must supply a name of a past individual")
    else:
        print('Loading genome:', args.load)

    if args.strict is not False and not isinstance(args.strict, bool):
        raise argparse.ArgumentTypeError("Must provide a boolean for strict breeding")

    return args


if __name__ == '__main__':
    main(parse_args())
