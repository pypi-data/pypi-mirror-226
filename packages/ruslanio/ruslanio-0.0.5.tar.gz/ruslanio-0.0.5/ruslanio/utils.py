import typing as tp


def flatten_list(l: tp.Any, times: int = -1):
    # Check exit contditions
    if times == 0:
        return l
    if not isinstance(l, list):
        if times >= 0:
            raise ValueError(f'{type(l)} is not list')
        else:
            return l

    # Flatten recursively
    new_l = []
    for sub_l in l:
        for item in sub_l:
            new_l.append(flatten_list(item, times - 1))
    return new_l
