from . import Extractor

def leniency(level):
    score = 0

    for column in level:
        if Extractor.contains_enemy(column):
            score += 0.5
        
        if Extractor.contains_gap(column):
            score += 0.5

    return score