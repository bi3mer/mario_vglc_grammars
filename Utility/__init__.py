from random import random
import sys

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

def update_progress(progress):
    '''
    modifed from: https://stackoverflow.com/questions/3160699/python-progress-bar
    NOTE: tqdm is better but avoiding dependencies for pypy
    '''
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    elif progress < 0:
        progress = 0
        status = "Halt...\r\n"
    elif progress >= 1:
        progress = 1
        status = "Done\r\n"

    block = int(round(barLength*progress))

    text = f'\rPercent [{"#"*block + "-"*(barLength-block)}] {round(progress*100, 2)}% {status}'
    sys.stdout.write(text)
    sys.stdout.flush()