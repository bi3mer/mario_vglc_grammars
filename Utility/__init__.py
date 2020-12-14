from random import random

def weighted_shuffle(items, weights):
    '''
    https://softwareengineering.stackexchange.com/a/344274
    '''
    order = sorted(range(len(items)), key=lambda i: -random() ** (1.0 / weights[i]))
    return [items[i] for i in order]

def columns_into_rows(columns):
    '''
    convert the column matrix into a string that can be easily viewed. 
    '''
    column_length = len(columns[0])
    rows = ["" for _ in range(column_length)]

    for col in columns:
        i = column_length - 1
        j = 0

        while i >= 0:
            rows[j] = f'{rows[j]}{col[i]}'

            i -= 1
            j += 1

    return '\n'.join(rows)

