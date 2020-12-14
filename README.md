# Mario VGLC + Grammars

## Getting Started

This repository uses the [VGLC](https://github.com/TheVGLC/TheVGLC.git) as a submodule. After pulling, you will need to run the two commands below for the code in this repo to work.

```bash
git submodule init
git submodule update
```

## Unit Tests

Run from the base directory.

```bash
python -m unittest test/*.py
```

## Functionality

This repo is designed to be a submodule for other work. 

### IO

IO allows you to grab a single mario level from the VGLC by name or the entire set. It reads into the format of a matrix. The first index is to the column. The second index is to the tiles in the column where `0` is the bottommost tile; this will generally be the ground tile. 

### Grammar

This contains implementations of n-grams and backoff n-grams. A brief introduction to n-grams and backoff n-grams can be found [here](https://bi3mer.github.io/blog/post_28/biemer_c_backoff_n_grams.pdf).

### Fitness

* BadTransitions uses a grammar—see above—to count the number of transitions that are not seen in the input dataset. THe grammar determines the size of `n`, not this function.
* Leniency calculates the the sum of leniency over every column. A column is scored based on the existence of an enemy and a gap. If an enemy exists, add `0.5`. Similarly, if a gap exists, add `0.5`. The max leniency of a column is `1`. The max leniency of a level is its length.
* Linearity calculates the line of best fit for the entire level and then compares it to the actual level. For each column, the absolute value of the difference between line of best fit and the max column height is used to calculate the score.
* Playability contains two different approaches. The first tries to count the number of unplayable columns. The second calculates the amount of the level that is expected to be traversable. Both of these are naive and not meant to be definitive. Their goal is to be quick approximations. 

### Generation

**Un-Constrained**

Unconstrained generation has the goal of generating a level of a certain size. It does not guarantee that a level of the requested size will be generated though. If the n-gram generates an unseen sequence then the constrained generation will stop there and return the level as is, regardless of length. This is best used for training scenarios where speed is important. 

**Constrained**

Constrained takes a start sequence and an end sequence and builds a path between the two with a breadth-first-search. The user can assign a minimum path length. If this is greater than 0, it will use unconstrained generation first to find the minimum length. After, it will use BFS.

## Examples

In the two examples below I use an n-gram for the first and a backoff for the second. This does not have to be the case, both will work in both scenarios.

### Unconstrained Generation

```python
from IO.GetLevels import get_single_super_mario_bros
from Generation.Unconstrained import generate
from Utility import columns_into_rows
from Grammar import NGram

level = get_single_super_mario_bros('mario-1-1.txt')
gram = NGram(3)
gram.add_sequence(level)

new_level = generate(gram, level[:4], 30)
print(columns_into_rows(new_level))
```

```
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------?-----
------------------------------
------------------------------
---S--------------------------
--------------X------Q--Q-----
--------------XX--------------
----------<>--XXX-------------
----------[]--XXXX----------E-
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Constrained

The array in the constructor for the backoff n-gram are the associated weights for each `n`. Normally, you'd want this to be intelligently chosen but we are generating and not concerned with the probability of a sequence.

```python
from IO.GetLevels import get_super_mario_bros
from Generation.Unconstrained import generate
from Generation.Constrained import generate_from_start_to_end
from Utility import columns_into_rows
from Grammar import BackoffNGram

levels = get_super_mario_bros()
gram = BackoffNGram(4, [1,0,0,0])
for lvl in levels:
    gram.add_sequence(lvl)

start = generate(gram, levels[0][:5], 10)
end = generate(gram, levels[-1][:5], 10)
new_level = generate_from_start_to_end(gram, start, end,10)
print(columns_into_rows(new_level))
```
```
-----------------------------------------
-----------------------------------------
-----------------------------------------
-----------------------------------------
-------------------------ooo-------------
-------------------------XXX-------------
-----------------------------------------
-----------------------------------------
----------------------------------oo-----
---QQQQ----------EE-E--------------------
--------------XXXXXXXXXX?----------------
B--E-------------------------------------
b----------------------------------------
XXXXXXXXXXXXXX----------XXXX-XX-X----X-XX
```