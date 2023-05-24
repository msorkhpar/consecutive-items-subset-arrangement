from __future__ import annotations

import logging

import numpy as np

from utils.omit_non_intersecting_pairs import remove_non_intersecting_pairs

logger = logging.getLogger(__name__)


def generate_random_consecutive_items_edge_set(nodes: int, min_pairs: int, max_pairs: int) -> tuple[
    list[int | str], list[str], list[int, int], list[tuple[int | str, str]]
]:
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

    items = sorted(set(item for start, end in item_sets for item in range(start, end + 1)))

    # Create a list of players from 1 to the random number of pairs
    players = [f'P{i}' for i in range(1, len(item_sets) + 1)]

    # Create edge list of items connected to players using item_sets values
    edges = [(item, player) for i, player in enumerate(players) for item in range(item_sets[i][0], item_sets[i][1] + 1)]

    while len(items) < len(players):
        del items, players, item_sets, edges
        items, players, item_sets, edges = generate_random_consecutive_items_edge_set(nodes, min_pairs, max_pairs)

    return items, players, item_sets, edges
