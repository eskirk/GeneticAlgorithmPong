from neuralnet import NeuralNet


class NeuralNetBreeder:
    def __init__(self, population_size):
        self.population = []
        self.generation = 0
        self.population_size = population_size

    def start_breeding(self):
        self.create_new_population()

        while True:
            for network in self.population:
                # play the game using this neural net and record the fitness function
                network.play_game()

            best_network = self.breed_best()
            best_network.mutate()
            self.create_new_population(starting_network=best_network)
            self.generation += 1

    def create_new_population(self, starting_network=None):
        population = []
        temp_population_size = self.population_size
        if starting_network:
            population.append(starting_network)
            temp_population_size -= 1

        for ndx in range(temp_population_size):
            network = NeuralNet()
            network.randomize()

            population.append(network)

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





