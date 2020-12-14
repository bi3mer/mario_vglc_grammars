from random import choices, sample

class UniGram():
    __slots__ = ['keys', 'counts', 'sum_counts', 'n']

    def __init__(self):
        self.keys = None
        self.counts = {}
        self.sum_counts = 0
        self.n = 1

    def add_sequence(self, sequence):
        self.sum_counts += len(sequence)

        for token in sequence:
            if token in self.counts:
                self.counts[token] += 1
            else:
                self.counts[token] = 1

        self.keys = list(self.counts.keys())

    def get_probability(self, token):
        if token in self.counts:
            return self.counts[token] / self.sum_counts
        return 0

    def has_next_step(self, sequence=None):
        return self.sum_counts > 0

    def get_output(self, sequence=None):
        return choices(self.keys, weights=self.counts.values())[0]

    def get_weighted_output(self, sequence=None):
        # NOTE: this should be updated to return a weighted order instead of one
        # that random
        return sample(self.keys, k=len(self.keys))
