from collections import deque

def bad_transitions(level, grammar):
    max_length = grammar.n - 1
    queue = deque([], maxlen=max_length)
    append_to_queue = queue.append
    bad_transitions = 0

    for token in level:
        if len(queue) == max_length:
            input_sequence = ','.join(list(queue))
            if input_sequence not in grammar.grammar:
                bad_transitions += 1

        append_to_queue(token)

    return bad_transitions