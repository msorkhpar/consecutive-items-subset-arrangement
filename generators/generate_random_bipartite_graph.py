from __future__ import annotations

import logging

import networkx as nx
import numpy as np
from networkx.algorithms import bipartite

logger = logging.getLogger(__name__)


def generate_random_edge_set(nodes: int, min_pairs: int, max_pairs: int) -> nx.Graph:
    num_pairs = np.random.randint(min_pairs, max_pairs + 1)
    return bipartite.gnmk_random_graph(nodes, num_pairs, np.random.randint(num_pairs * 3, num_pairs * 7))
