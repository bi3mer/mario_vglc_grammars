from collections import deque
from random import choices
from math import isclose, log, exp

from .UniGram import UniGram

class BackoffNGram:
    '''
    Could be improved to use a smoothing method.
    '''
    __slots__ = ['n', 'grammar', 'unigram', 'weights']

    def __init__(self, size, weights):
        assert len(weights) == size
        assert isclose(1, sum(weights))

        self.n = size
        self.grammar = {}
        self.unigram = UniGram()
        self.weights = weights

    def add_sequence(self, sequence):
        self.unigram.add_sequence(sequence)

        for n in range(1, self.n):
            queue = deque([], maxlen=n)
            append_to_queue = queue.append

            for token in sequence:
                if len(queue) == n:
                    key = ','.join(queue)
                    if key not in self.grammar:
                        self.grammar[key] = { token: 1 }
                    elif token not in self.grammar[key]:
                        self.grammar[key][token] = 1
                    else:
                        self.grammar[key][token] += 1

                append_to_queue(token)

    def has_next_step(self, sequence):
        return self.unigram.has_next_step()

    def get_output(self, sequence):
        split_sequence = sequence.split(',')

        while len(split_sequence) >= 1:
            input_sequence = ','.join(split_sequence)
            if input_sequence in self.grammar:
                unigram = self.grammar[input_sequence]
                return choices(list(unigram.keys()), weights=unigram.values())[0]

            split_sequence.pop(0)

        return self.unigram.get_output()

    def get_unweighted_output(self, sequence):
        split_sequence = sequence.split(',')

        while len(split_sequence) >= 1:
            input_sequence = ','.join(split_sequence)
            if input_sequence in self.grammar:
                unigram = self.grammar[input_sequence]
                return list(unigram.keys())

            split_sequence.pop(0)

        return self.unigram.get_output()

    def get_probability(self, split_sequence, output):
        '''
        used by sequence_probability to get the probability of the output given
        the input sequence.
        '''
        while len(split_sequence) >= 1:
            input_sequence = ','.join(split_sequence)
            if input_sequence in self.grammar:
                unigram = self.grammar[input_sequence]

                if output in unigram:
                    return self.weights[len(split_sequence)] * unigram[output] / sum(unigram.values())

            split_sequence.pop(0)

        return self.weights[0] * self.unigram.get_probability(output)

    def sequence_probability(self, sequence):
        if not self.unigram.has_next_step():
            return 0

        max_length = self.n - 1
        queue = deque([], maxlen=max_length)
        append_to_queue = queue.append
        probability = 0

        for token in sequence:
            likelihood = self.get_probability(list(queue), token)
            if likelihood == 0:
                return 0

            probability += log(likelihood)
            append_to_queue(token)

        return exp(probability)