from collections import deque
import random

from Utility.Extractor import contains_enemy, contains_gap, max_height
from Utility.List import weighted_shuffle
from NGram import BackoffNGram

from .Unconstrained import generate


def get_column_scores(column):
    column_leniency = 0
    if contains_enemy(column):
        column_leniency += 0.5
    
    if contains_gap(column):
        column_leniency += 0.5

    return column_leniency, max_height(column)

def generate_backoff(grammar, input_sequence, linearity, leniency, always_use_unigram=True):
    '''
    This must be run with a backoff n-gram else there will be an error.

    linearity will be the expected height of the column
    leniency will be the expected leniency of the column
    '''
    prior = deque(input_sequence, maxlen=grammar.n - 1)
    prior_val = list(prior)
    output = []

    for i in range(len(linearity)):
        expected_height = linearity[i]
        expected_leniency = leniency[i]

        closest_column = None
        closest_distance = 1000000

        output_column = None
        for n in reversed(range(grammar.n)):
            input_sequence = ','.join(prior_val[-(n - 1):])

            if input_sequence not in grammar.grammar:
                continue

            unigram = grammar.grammar[input_sequence]
            choices = weighted_shuffle(list(unigram.keys()), list(unigram.values()))

            for column in choices:
                column_leniency, column_height = get_column_scores(column)

                if column_height == expected_height and column_leniency == expected_leniency:
                    output_column = column
                    break

                new_distance = .5 * abs(expected_leniency - column_leniency) + \
                               .5 * abs(column_height - expected_height)

                if new_distance < closest_distance:
                    closest_distance = new_distance
                    closest_column = column

            if output_column != None:
                break

        if output_column == None:
            if always_use_unigram or closest_column == None:
                choices = grammar.unigram.get_weighted_output()

                for column in choices:
                    column_leniency, column_height = get_column_scores(column)

                    if column_height == expected_height and column_leniency == expected_leniency:
                        output_column = column
                        break

                    new_distance = .5 * abs(expected_leniency - column_leniency) + \
                                .5 * abs(column_height - expected_height)

                    if new_distance < closest_distance:
                        closest_distance = new_distance
                        closest_column = column

            if output_column == None:
                if closest_column == None:
                    output_column = grammar.get_output(','.join(prior_val))
                else:
                    output_column = closest_column
    
        output.append(output_column)
        prior.append(output_column)

        prior_val = list(prior)

    return output

def generate_from_start_to_end(grammar, start, end, min_length, max_length):
    # generate path of minimum length with an n-ram
    min_path = start + generate(grammar, start, min_length)

    # BFS to find the ending prior
    path_found = False
    queue = deque()
    came_from = {}

    start_prior = ','.join(min_path[-(grammar.n - 1):])
    end_prior = ','.join(end[:grammar.n - 1])

    queue.append(start_prior)

    while queue:
        prior = queue.popleft()
        split_prior = prior.split(',')

        output = grammar.get_unweighted_output(prior)
        if output != None:
            for new_column in output:
                new_prior_queue = deque(split_prior, maxlen=grammar.n - 1)
                new_prior_queue.append(new_column)
                new_prior = ','.join(list(new_prior_queue))

                if new_prior not in came_from:
                    came_from[new_prior] = split_prior
                    if new_prior == end_prior:
                        path_found = True
                        break
                    else:
                        queue.append(new_prior)
            
            if path_found:
                break
    
    if not path_found:
        return None

    # reconstruct path and cut off tail if past max_length
    path = []
    current = end_prior

    while current != start_prior:
        path.insert(0, current.split(',')[-1])
        current = ','.join(came_from[current])
        
    return (min_path + path + end[grammar.n - 1:])[:max_length]