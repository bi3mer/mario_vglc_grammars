from .Utility import columns_into_rows
from .Extractor import min_height, max_height, heights as eHeights
from .ModifiedAStar import percent_completable

def playability(columns):
    '''
    NOTE: this is purposely naive, it is not supposed to be complete or truly
    guarantee playability. This is an approximation.

    - You need to make sure that a player can get from start to end
    - pipes should always be complete
    '''
    unplayable_elements_found = 0

    column_iter = iter(columns)
    col = next(column_iter)

    current_height = max_height(col)
    gaps_seen = 0 if current_height != -1 else 1
    pipe_starts = []
    for i in range(len(col)):
        if col[i] == '[':
            pipe_starts.append(i)

    for col in columns:
        # handle height
        heights = eHeights(col)

        if len(heights) == 0:
            gaps_seen += 1

            if gaps_seen > 4:
                unplayable_elements_found += 1
        else:
            gaps_seen = 0

            valid_height = -1
            for h in heights:
                if not (h > current_height + 4):
                    valid_height = h
                    break

            if valid_height == -1:
                current_height = valid_height
                unplayable_elements_found += 1
            else:
                current_height = heights[0]

        # handle pipes
        for i in pipe_starts:
            if col[i] != ']':
                unplayable_elements_found += 1 
                break

        pipe_starts = []
        for i in range(len(col)):
            if col[i] == '[':
                pipe_starts.append(i)

    return unplayable_elements_found

def expected_playability(linearity_list):
    height_iterator = iter(linearity_list)
    height = next(height_iterator)
    unplayability = 0

    for h in height_iterator:
        if h > height + 4:
            unplayability += 1
        
        height = h

    return unplayability

def percent_playable(columns):
    '''
    This uses an A* agent to tell if a level is playable. It should be pretty
    close to perfect.
    '''
    w = 0
    h = 0
    start_found = False

    while not start_found:
        h = min_height(columns[w])

        if h != -1:
            h = len(columns[0]) - 2 - h
            start_found = True
        else:
            w += 1
    
    return percent_completable(10, (w, h, -1), columns_into_rows(columns))

def naive_percent_playable(columns):
    '''
    This uses an approximation. It is not perfect. It is meant to be fast. Use
    percent_playable for a perfect score.
    '''
    column_iter = iter(columns)
    col = next(column_iter)

    current_height = max_height(col)
    gaps_seen = 0 if current_height != -1 else 1

    for i, col in enumerate(columns):
        heights = eHeights(col)

        if len(heights) == 0:
            gaps_seen += 1

            if gaps_seen > 6:
                break
        else:
            valid_height = -1
            for h in heights:
                if not (h > current_height + 4):
                    valid_height = h
                    break

            if valid_height == -1:
                current_height = valid_height
                gaps_seen += 1
            else:
                current_height = heights[0]
                gaps_seen = 0

    if i == len(columns) - 1:
        return 1.0 # remove rounding error for unit tests

    return i / len(columns)