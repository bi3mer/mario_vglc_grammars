from .BackoffNGram import BackoffNGram
from .UniGram import UniGram
from .NGram import NGram

def build(size):
    if size == 1:
        return UniGram()

    return NGram(size)

def build_backoff(size, weights):
    if size == 1:
        return UniGram()

    return BackoffNGram(size, weights)

def build_interpolated(size):
    pass