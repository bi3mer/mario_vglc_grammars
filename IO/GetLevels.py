import os

def rows_into_columns(rows):
    iter_rows = iter(rows)
    columns = [token for token in next(iter_rows).strip()]

    for row in iter_rows:
        row = row.strip()
        for i in range(len(row)):
            columns[i] = f'{row[i]}{columns[i]}'

    return columns

def columns_into_rows(columns):
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

def get_super_mario_bros():
    path = os.path.join("TheVGLC", "Super Mario Bros", "Processed")
    skip_levels = ['mario-1-2.txt', 'mario-2-1.txt' 'mario-4-2.txt', 'mario-4-3.txt', 
                   'mario-5-3.txt', 'mario-6-3.txt']
    levels = []

    for file_name in os.listdir(path):
        if file_name in skip_levels:
            continue

        f = open(os.path.join(path, file_name))
        levels.append(rows_into_columns(f.readlines()))
        f.close()

    return levels

def get_single_super_mario_bros(level_name):
    path = os.path.join("TheVGLC", "Super Mario Bros", "Processed")
    f = open(os.path.join(path, level_name))
    lvl = rows_into_columns(f.readlines())
    f.close()

    return lvl