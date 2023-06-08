from __future__ import annotations

import logging
import random

import networkx as nx
import numpy as np
from networkx.algorithms import bipartite

logger = logging.getLogger(__name__)


def generate_random_edge_set(min_players: int, max_players: int, min_items: int, max_items: int,
                             min_number_of_edges: int, max_number_of_edges: int) -> nx.Graph:
    num_of_players = random.randint(min_players, max_players + 1)
    num_of_items = random.randint(min_items, max_items + 1)
    num_of_edges = random.randint(min_number_of_edges, max_number_of_edges+1)
    return bipartite.gnmk_random_graph(num_of_players, num_of_items, num_of_edges)
