import collections
from itertools import tee


def ensure_tuple(value):
    if isinstance(value, tuple):
        return value
    elif isinstance(value, collections.Iterable):
        return tuple(value)
    else:
        return (value,)


def pairize(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    pairs = []
    a = iter(iterable)
    try:
        while True:
            pairs.append((next(a), next(a)))
    except StopIteration:
        return pairs

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
