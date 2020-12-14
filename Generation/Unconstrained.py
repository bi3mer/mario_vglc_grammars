from collections import deque

def generate(grammar, input_sequence, size):
    prior = deque(input_sequence, maxlen=grammar.n - 1)
    prior_val = ','.join(list(prior))
    output = []

    while len(output) < size and grammar.has_next_step(prior_val):
        new_token = grammar.get_output(prior_val)
        output.append(new_token)
        prior.append(new_token)

        prior_val = ','.join(list(prior))

    return output