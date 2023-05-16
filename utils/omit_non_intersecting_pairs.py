from collections import OrderedDict

import pandas as pd


def remove_non_intersecting_pairs(item_sets: list[tuple[int, int]]):
    # Create a DataFrame from the list of pairs
    df = pd.DataFrame(item_sets, columns=["start", "end"])

    # Check for overlapping pairs
    overlapping = df.apply(lambda row: df[(row.start <= df.end) & (df.start <= row.end)].shape[0] > 1, axis=1)

    # Convert the filtered DataFrame back to a list of pairs
    item_sets = df[overlapping].apply(tuple, axis=1).tolist()
    item_sets.sort()

    return item_sets
