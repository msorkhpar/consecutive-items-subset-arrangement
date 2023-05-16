import networkx as nx

from utils.random_sets import generate_k_numbers_with_total_sum_m


def assign_random_values_to_item_set(G: nx.Graph):
    items = [node for node, attr in G.nodes(data=True) if attr['bipartite'] == 0]
    players = [node for node, attr in G.nodes(data=True) if attr['bipartite'] == 1]
    nx.set_node_attributes(G, {
        item: {'value': num} for item, num in
        zip(items,
            generate_k_numbers_with_total_sum_m(len(items), len(players)))
    })
