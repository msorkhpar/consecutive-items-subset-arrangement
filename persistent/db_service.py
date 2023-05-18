from __future__ import annotations

import networkx as nx

from persistent.models.BaseModel import BaseModel

from persistent.models.BipartiteGraph import BipartiteGraph
from utils.graph_db_coverter import graph_to_db_fields_converter, values_to_json_array


def create_tables():
    with BaseModel.get_db() as db:
        BaseModel.create_tables()


def persist_fractional_solution(bigraph_id: int, k: float, values: dict[tuple[str, str], float], time: float):
    with BaseModel.get_db() as db:
        bigraph = BipartiteGraph.get(BipartiteGraph.bigraph_id == bigraph_id)
        bigraph.fractional_k = k
        bigraph.fractional_solution_time = time
        # bigraph.fractional_values = values_to_json_array(values)
        bigraph.save()


def persist_integral_solution(bigraph_id: int, k: float, values: dict[tuple[str, str], float], time: float):
    with BaseModel.get_db() as db:
        bigraph = BipartiteGraph.get(BipartiteGraph.bigraph_id == bigraph_id)
        bigraph.integral_k = k
        bigraph.integral_solution_time = time
        # bigraph.integral_values = values_to_json_array(values)
        bigraph.save()


def persist_bigraph(G: nx.Graph) -> int:
    items, players, item_sets, edges = graph_to_db_fields_converter(G)
    with BaseModel.get_db() as db:
        g = BipartiteGraph(
            number_of_items=len(items),
            number_of_players=len(players),
            number_of_edges=len(edges),
            items=items,
            item_sets=item_sets,
            # players=players,
            # edges=edges,
        )
        g.save()
        return g.bigraph_id
