import collections


def ensure_array(value):
    return value if isinstance(value, collections.Iterable) else (value,)


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    pairs = []
    a = iter(iterable)
    try:
        while True:
            pairs.append((next(a), next(a)))
    except StopIteration:
        return pairs
