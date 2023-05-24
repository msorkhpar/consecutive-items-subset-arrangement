from __future__ import annotations

import networkx as nx


def construct_bipartite_graph(items: list, players: list, edges: list[tuple[str | int, str]],
                              values: list[float] = None) -> nx.Graph:
    # Create a bipartite graph
    G = nx.Graph()

    # Add the nodes and edges
    if values is None:
        G.add_nodes_from(items, bipartite=0)
    else:
        G.add_nodes_from((item, {"bipartite": 0, "value": value}) for item, value in zip(items, values))

    G.add_nodes_from(players, bipartite=1)
    G.add_edges_from(edges)
    return G
