import networkx as nx
import numpy as np


def assign_random_values_to_item_set(G: nx.Graph):
    nx.set_node_attributes(G, {
        node: {'value': np.round(np.random.uniform(0, 1), 5)} for node, attr in G.nodes(data=True)
        if attr['bipartite'] == 0
    })
