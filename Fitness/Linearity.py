from . import Extractor

def get_slope_and_intercept(x, y):
    sum_x = 0
    sum_y = 0
    sum_x_squared = 0
    sum_xy = 0

    n = len(x)
    for i in range(n):
        x_val = x[i]
        y_val = y[i]

        sum_x += x_val
        sum_x_squared += pow(x_val, 2)
        sum_xy += x_val * y_val
        sum_y += y_val

    # y = mx + b
    denominator  =  ((n * sum_x_squared) - pow(sum_x, 2))
    if denominator == 0:
        return 0, 0

    m = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x_squared) - pow(sum_x, 2))
    b = (sum_y - (m * sum_x)) / n
    return m, b

def linearity_with_heights(heights):
    '''
    a gap is not supposed to be included in the linearity calculation. The input
    for least squares is offset to accommodate this.
    '''
    x = []
    y = []

    subtract_by = 0
    for i in range(len(heights)):
        h = heights[i]

        if h != -1:
            x.append(i - subtract_by)
            y.append(h)
        else:
            subtract_by += 1

    slope, expected = get_slope_and_intercept(x, y)
    score = 0

    for height in y:
        if height != -1:
            score += abs(expected - height)
            expected += slope

    return score

def linearity(level):
    return linearity_with_heights([Extractor.min_height(col) for col in level])

def percent_linearity(level):
    return linearity(level) / max_linearity(len(level), len(level[0]))
    
def max_linearity(level_size, level_height):
    expected = level_height / 2
    h = 0
    score = 0

    for _ in range(level_size):
        score += abs(expected - h)

        if h == 0:
            h = level_height - 1
        else:
            h = 0

    return score