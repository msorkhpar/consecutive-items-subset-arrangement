import numpy as np

from utils.omit_non_intersecting_pairs import remove_non_intersecting_pairs


def generate_random_edge_set(nodes, min_pairs, max_pairs):
    # Pick a random number of pairs between min_pairs and max_pairs
    num_pairs = np.random.randint(min_pairs, max_pairs + 1)

    item_sets = []
    while len(item_sets) <= 1:
        # Create a list of randomly generated node pair ranges
        item_sets = list(
            map(
                lambda start: (start, np.random.randint(start + 2, nodes + 1)),
                np.random.randint(1, nodes - 2, size=num_pairs)
            )
        )

        # Sort the items pairs by their starting range and remove non-intersecting pairs
        item_sets = remove_non_intersecting_pairs(item_sets)

    items = sorted(set(num for start, end in item_sets for num in range(start, end + 1)))

    # Create a list of players from 1 to the random number of pairs
    players = [f'P{i}' for i in range(1, len(item_sets) + 1)]

    # Create edge list of items connected to players using item_sets values
    edges = [(j, player) for i, player in enumerate(players) for j in range(item_sets[i][0], item_sets[i][1] + 1)]

    return items, players, edges
