import networkx as nx
import numpy as np


def ceiling_big_item_values(G: nx.Graph):
    nx.set_node_attributes(G, {
        node: {'value': 1.0} for node, attr in G.nodes(data=True)
        if attr['bipartite'] == 0 and attr['value'] >= (1/3)
    })
