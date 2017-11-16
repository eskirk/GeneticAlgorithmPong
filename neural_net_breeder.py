from neuralnet import NeuralNet, AIPaddle, NNPaddle
from pong import PongGame
import copy
import random


class NeuralNetBreeder:
    def __init__(self, population_size=10, strict_breeding=False):
        self.population = []
        self.games = []
        self.generation = 0
        self.best = []
        self.population_size = population_size
        self.cur_speed = 1000
        self.strict_breeding = strict_breeding

    def start_breeding(self, parent=None):
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
            return sorted(population, key=lambda x: x.fitness, reverse=True)
        elif parent is not None:
            population = [parent]
            game = PongGame()
            parent.game = game
            parent.ball = game.ball
            game.paddle1 = parent

            self.games = [game]
            for i in range(self.population_size - 1):
                population.append(self.crossover(parent))
            return population

    def create_new_population(self):
        print('\nCreating new population of size', self.population_size)
        self.generation = 0
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

        if parent2 is None:
            mate = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, offspring.game.ball, offspring.game)
        else:
            mate = parent2
        offspring.fitness = 0
        offspring.generation = parent1.generation + 1

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

    def play_games(self):
        # iterate the generation count
        self.generation += 1
        # if nobody survived the last generation, generate a new population
        if len(self.population) == 0:
            print('\nCreating new population')
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
            print('\nGeneration', self.games[0].paddle1.generation)
            for game in self.games:
                game.paddle2.ball = game.ball
                game.paddle2.score = 0
                game.paddle1.score = 0
                game.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, game.ball)
                game.speed = self.cur_speed
                game.start_game()
                print(game.paddle1)
                self.cur_speed = game.speed
        # start breeding the newly evaluated genomes
        return self.breed()

    def breed(self):
        fit_individuals = []
        for p in self.population:
            if self.strict_breeding:
                if p.fitness > 1:
                    fit_individuals.append(p)
            else:
                p.fitness += p.contacts_ball
                if p.fitness > 1:
                    fit_individuals.append(p)
        self.population = []
        self.games = []

        if len(fit_individuals) >= 1:
            fit_individuals = sorted(fit_individuals, key=lambda x: x.fitness, reverse=True)
            fittest = fit_individuals[0]
            if len(fit_individuals) == 1:
                while len(self.population) < self.population_size:
                    self.population.append(self.crossover(fittest))
            else:
                second_fittest = fit_individuals[1]
                fittest = self.crossover(fittest, second_fittest)
                while len(self.population) < self.population_size:
                    self.population.append(self.crossover(fittest))
            return fittest
        return None


def main(args):
    parent = None
    breeder = NeuralNetBreeder(args.p)
    if args.load is not None:
        parent = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, None, None)
        parent.load_genomes(args.load)
        parent.generation = 0

    breeder.population = breeder.start_breeding(parent)

    while breeder.generation < args.g:
        # play the games and evolve if any of the genomes are successful
        best = breeder.play_games()
        if best is not None:
            best.save_genome()
            print('\nDaddy of generation', best.generation + 1, '-', best)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', type=int, default=5)
    parser.add_argument('-p', type=int, default=10)
    parser.add_argument('-load', type=str, default=None)
    parser.add_argument('-strict', type=bool, default=False)
    args = parser.parse_args()

    if args.g <= 0:
        raise argparse.ArgumentTypeError("Minimum generations is 1")

    if args.g <= 0:
        raise argparse.ArgumentTypeError("Minimum population size is 1")

    if args.load is not None and not isinstance(args.load, str):
        raise argparse.ArgumentTypeError("Must supply a name of a past individual")
    else:
        print('Loading genome:', args.load)

    if args.strict is not False and not isinstance(args.strict, bool):
        raise argparse.ArgumentTypeError("Must provide a boolean for strict breeding")

    main(args)







