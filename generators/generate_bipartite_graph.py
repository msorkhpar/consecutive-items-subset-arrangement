import networkx as nx


def construct_bipartite_graph(items, players, edges):
    # Create a bipartite graph
    G = nx.Graph()

    # Add the nodes and edges
    G.add_nodes_from(items, bipartite=0)
    G.add_nodes_from(players, bipartite=1)
    G.add_edges_from(edges)
    return G
