from collections import deque
from random import choices
from math import log, exp

class NGram():
    __slots__ = ['input_size', 'n', 'grammar']

    def __init__(self, size):
        self.input_size = size - 1
        self.n = size
        self.grammar = {}

    def add_sequence(self, sequence):
        queue = deque([], maxlen=self.input_size)

        for token in sequence:
            if len(queue) == queue.maxlen:
                key = ','.join(queue)
                if key not in self.grammar:
                    self.grammar[key] = { token: 1 }
                elif token not in self.grammar[key]:
                    self.grammar[key][token] = 1
                else:
                    self.grammar[key][token] += 1

            queue.append(token)

    def has_next_step(self, sequence):
        return sequence in self.grammar

    def get_output(self, sequence):
        unigram = self.grammar[sequence]
        return choices(list(unigram.keys()), weights=unigram.values())[0]

    def get_weighted_output(self, sequence):
        if sequence not in self.grammar:
            return None

        unigram = self.grammar[sequence]
        keys = list(unigram.keys())
        keys.sort(key=lambda k: -unigram[k])
        return keys

    def get_unweighted_output(self, sequence):
        if sequence not in self.grammar:
            return None
            
        unigram = self.grammar[sequence]
        return list(unigram.keys())

    def get_probability(self, split_input, output):
        probability = 0
        input_sequence = ','.join(split_input)
        if input_sequence in self.grammar:
            unigram = self.grammar[input_sequence]
            if output in unigram:
                probability = unigram[output] / sum(unigram.values())

        return probability

    def sequence_probability(self, sequence):
        max_length = self.n - 1
        queue = deque([], maxlen=max_length)
        append_to_queue = queue.append
        probability = 0

        for token in sequence:
            if len(queue) == max_length:
                likelihood = self.get_probability(list(queue), token)
                if likelihood == 0:
                    return 0
                    
                probability += log(likelihood)
            append_to_queue(token)

        return exp(probability)