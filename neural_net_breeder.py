from neuralnet import NeuralNet, AIPaddle, NNPaddle
from pong import PongGame
from ball import Ball


class NeuralNetBreeder:
    def __init__(self, population_size):
        self.population = []
        self.games = []
        self.generation = 0
        self.population_size = population_size

    def start_breeding(self):
        self.create_new_population()
        winners = []

        for game in self.games:
            # play the game using this neural net and record the fitness function
            game.play_game()
            while not game.game_over:
                pass
            winners.append(game.winner)
        print(winners)

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

    def breed_best(self):
        best, next_best = self.population.sort(reverse=True)[:2]

        # neural net sex

        # return super child

        return best  # need to actually do the sex part

    # set current genome fit, if all genomes have been set,
    # create a new generation
    def new_genome(self, current_fit):
        pass

    # create a new generation, if the generation has already been initialized,
    # crossover to create a new generation
    def new_generation(self):
        pass

    # sort the genomes and cross them over with all other genomes
    def crossover(self):
        pass

    def randomize(self):
        pass

    def mutate(self):
        pass


if __name__ == '__main__':
    breeder = NeuralNetBreeder(10)
    breeder.start_breeding()




