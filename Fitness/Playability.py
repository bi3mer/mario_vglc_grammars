from . import Extractor

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

    current_height = Extractor.max_height(col)
    gaps_seen = 0 if current_height != -1 else 1
    pipe_starts = []
    for i in range(len(col)):
        if col[i] == '[':
            pipe_starts.append(i)

    for col in columns:
        # handle height
        heights = Extractor.heights(col)

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
    column_iter = iter(columns)
    col = next(column_iter)

    current_height = Extractor.max_height(col)
    gaps_seen = 0 if current_height != -1 else 1

    for i, col in enumerate(columns):
        heights = Extractor.heights_with_enemies(col)

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

