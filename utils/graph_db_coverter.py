from __future__ import annotations

from dataclasses import asdict

import networkx as nx

from persistent.models.BipartiteGraph import BipartiteGraph


def values_to_json_array(values: dict[tuple[str, str], float]):
    json_array = list()
    for (from_node, to_node), value in values.items():
        json_array.append({'f': from_node, 't': to_node, 'v': value})
    return json_array


def graph_to_db_fields_converter(G: nx.Graph):
    items = list()
    players = list()
    edges = list()
    item_index = 0
    player_index = 0

    for node, attributes in G.nodes(data=True):
        if attributes['bipartite'] == 0:
            items.append(asdict(BipartiteGraph.Item(node, attributes['value'])))
            item_index += 1
        elif attributes['bipartite'] == 1:
            players.append(asdict(BipartiteGraph.Player(node)))
            player_index += 1

    item_sets = dict()
    for item, player in G.edges():
        edges.append(asdict(BipartiteGraph.Edge(item, player)))
        item_sets.setdefault(player, list()).append(item)

    item_sets = [asdict(BipartiteGraph.ItemSet(min(items), max(items)))
                 for index, (player, items) in enumerate(item_sets.items())]

    return items, players, item_sets, edges


def db_fields_to_graph_converter(db_graph: BipartiteGraph):
    G = nx.Graph()

    for item in db_graph.get_items():
        G.add_node(item.node, bipartite=0, value=item.value)

    for player in db_graph.get_players():
        G.add_node(player.node, bipartite=1)

    for edge in db_graph.get_edges():
        G.add_edge(edge.from_node, edge.to_node)

    return G
