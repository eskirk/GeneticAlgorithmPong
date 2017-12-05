import math

from neuron import Neuron
from synapse import Synapse


class NeuralNet(object):
    def __init__(self, num_inputs, num_hidden_layers, num_neurons):
        self.fitness = None
        self.output = Neuron()
        self.inputs = [Neuron() for _ in range(num_inputs)]
        self.hidden_layers = [[Neuron() for _ in range(num_neurons)]
                              for _ in range(num_hidden_layers)]
        self.synapses = [[] for _ in range(num_hidden_layers + 1)]
        self.num_hidden_layers = num_hidden_layers
        self.init_synapses()

    def init_synapses(self):
        # link inputs and first hidden layer
        for input_ndx, input_neuron in enumerate(self.inputs):
            for neuron in self.hidden_layers[0]:
                self.synapses[0].append(Synapse(input_neuron, neuron))

        # link hidden layers to each other
        if len(self.hidden_layers) > 1:
            for curr_ndx in range(len(self.hidden_layers) - 1):
                for neuron in self.hidden_layers[curr_ndx]:
                    for next_neuron in self.hidden_layers[curr_ndx + 1]:
                        self.synapses[curr_ndx + 1].append(Synapse(neuron, next_neuron))

        # link last layer to output
        for neuron in self.hidden_layers[len(self.hidden_layers) - 1]:
            self.synapses[len(self.synapses) -
                          1].append(Synapse(neuron, self.output))

    def get_output(self, inputs):
        # set the value of the input neurons to the input values passed in
        for inp in enumerate(inputs):
            self.inputs[inp[0]].set_value(inp[1])

        # go through each of the synapses and add the values to the next layer of neurons
        for i in range(self.num_hidden_layers):
            for synapse in self.synapses[i]:
                synapse.end_neuron.add_value(
                    synapse.weight * synapse.start_neuron.get_value())
            # once all the values have been added together, apply the sigmoid to the final value of the neuron
            for neuron in self.hidden_layers[i]:
                neuron.set_value(NeuralNet.sigmoid(neuron.get_value()))

        # generate the final value by adding all the final layers values together
        for synapse in self.synapses[self.num_hidden_layers]:
            synapse.end_neuron.add_value(
                synapse.weight * synapse.start_neuron.get_value())

        # apply the sigmoid function to the final neuron's value
        self.output.set_value(NeuralNet.sigmoid(self.output.get_value()))
        # print(self.output, ' final layer, post sigmoid')

        return self.output.get_value()

    @staticmethod
    def sigmoid(x):
        if x > 700:
            x = 700
        elif x < -700:
            x = -700
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            print(x, ' overflow')
            x = -x
            return 1 / (1 + math.exp(x))
