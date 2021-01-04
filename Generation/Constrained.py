from collections import deque
from .Unconstrained import generate

def generate_from_start_to_end(grammar, start, end, min_length, include_path_length=False):
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

    # reconstruct path
    path = []
    current = end_prior

    while current != start_prior:
        path.insert(0, current.split(',')[-1])
        current = ','.join(came_from[current])
    
    full_map = min_path + path[:len(path) - min(len(path) - 1, grammar.n - 1)] + end
    if include_path_length:
        return full_map, len(full_map) - len(start) - len(end)
    
    return full_map