from IO.GetLevels import get_single_super_mario_bros
from Generation.Unconstrained import generate
from Utility import columns_into_rows
from Grammar import NGram

level = get_single_super_mario_bros('mario-1-1.txt')
gram = NGram(3)
gram.add_sequence(level)

new_level = generate(gram, level[:4], 30)
print(columns_into_rows(new_level))