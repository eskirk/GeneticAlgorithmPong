# Genetic Algorithm Plays Pong
By [Elliot Kirk](https://github.com/eskirk) and [Colin Dutter](https://github.com/collindutter)
## Prerequisites 
- [Python3](https://www.python.org/downloads/)
- [Pygame](http://www.pygame.org/download.shtml)

## How to Run the Neural Net Breeder
 * From the directory you cloned this repo into, run `python3 breeder.py`
 * There are a couple of optional arguments you can include:
    * `-g, int`: specifies the number of generations to evolve over
        * `default = 5`
    * `-p, int`: specifies the size of each population (must be even)
        * `default = 10`
    * `-load, string`: specifies a specific genome (located in the `/genomes` folder) to start a new generation from
        * `default = None`
             * the user can provide a list of names to load multiple genomes at once (ex. `-load '[Name1, Name2, ...]'`)
    * `-strict, boolean`: specify whether or not you want strict breeding (use a fitness function based only on scoring 
    points, excluding the number of times the individual hits the ball)
        * `default = True` for the first generation, `False` for subsequent generations 
    * `-arena, boolean`: enable the dreaded arena mode; a free-for-all four-paddle version of pong 
        * `default = False`
    
 ## How the Genetic Algorithm Works
 This program uses a neural net in combination with a genetic algorithm to find the ultimate pong-playing AI.
 
 The genetic algorithm initially produces a random list of weights (`floats` in the range [0, 1]) and uses those values 
 as the weights on the synapses of a neural network.
 
 At the end of each generation, the fitness of all the members of the population are evaluated
 * if no individuals score a point, a new population is generated, `strict_breeding` is set to False, and the generation count is set to 0, 
 * if only one individual scores a point, random mates are created and crossed over with the winner to create a new population
 * if more than one individual scores a point, those individuals will mate and create a new population from their genomes
   
 If the population makes it past the second generation on their own, they start to play themselves rather than the basic AI  
 Once the generation count hits the value specified in `-g`, the simulation ends and the fittest individual's genes are saved into `/genomes`
 
 ## In-Game Controls
 * `Up` moves the player controlled paddle up
 * `Down` moves the player controlled paddle down
 * `Left` slows down the game
 * `Right` speeds up the game
 * `R` resets the current game
 * `P` pauses the current game
 * `Space` allows the user to take control of the paddle on the left
 
 ## Resources
 If you are interested in this project but don't know where to get started, don't worry, we were there too. 
 To get started we did some research and came across a few good resources online.
 * [Pong Neural Network](https://www.youtube.com/watch?v=Hqf__FlRlzg)
    * This tutorial teaches you how to write a pong-playing AI using neural network libraries, rather than from scratch
 * [Neural Network plays Pong](https://github.com/fabiorino/NeuralNetwork-plays-Pong/blob/master/Pong/Pong.java)
    * Very similar project to this one, but written in Java
  
