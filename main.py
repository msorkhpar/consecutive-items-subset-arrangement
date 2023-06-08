import logging
import os
from dataclasses import dataclass
from multiprocessing.pool import Pool

import pandas as pd
from dotenv import load_dotenv

from generators.generate_bipartite_graph import construct_bipartite_graph
from generators.generate_consecutive_items_bipartite_graph import generate_random_consecutive_items_edge_set
from generators.generate_random_bipartite_graph import generate_random_edge_set
from transformers.assign_items_random_values import assign_random_values_to_item_set
from transformers.ceiling_big_items_values import ceiling_big_item_values
from lp.solver import Solver
from persistent.db_service import create_tables, persist_bigraph, persist_fractional_solution, persist_integral_solution

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=int(os.getenv('LOG_LEVEL')))
logger = logging.getLogger(__name__)


@dataclass
class ConsecutiveGraph:
    nodes: int
    min_pairs: int
    max_pairs: int


@dataclass
class RandomBiGraph:
    min_items: int
    max_items: int
    min_players: int
    max_players: int
    min_edges: int
    max_edges: int


def process_task(data):
    if type(data) is ConsecutiveGraph:
        items, players, item_sets, edges = generate_random_consecutive_items_edge_set(
            data.nodes, data.min_pairs, data.max_pairs
        )
        G = construct_bipartite_graph(items, players, edges)
        logger.info(f"A sample with {len(items)} items, {len(players)} players, and {len(edges)} edges is created.")
    else:
        G = generate_random_edge_set(
            data.min_items, data.max_items, data.min_players, data.max_players, data.min_edges, data.max_edges
        )
        logger.info(f"A sample random graph {G}] is created. ")

    assign_random_values_to_item_set(G)
    ceiling_big_item_values(G)

    lp_solver = Solver(G)
    fractional_solution = lp_solver.solve()
    if fractional_solution is None:
        return
    logger.info(f"Fractional K=[{fractional_solution.K}] has been found.")
    if fractional_solution.K == 1.0:
        lp_solver.change_to_integral()
        integral_solution = lp_solver.solve()
        if integral_solution is None:
            return
        logger.info(f"Integral K=[{integral_solution.K}] has been found.")
        if integral_solution.K >= 2:
            bigraph_id = persist_bigraph(G)
            persist_fractional_solution(
                bigraph_id, fractional_solution.K, fractional_solution.variables, fractional_solution.running_time
            )
            persist_integral_solution(
                bigraph_id, integral_solution.K, integral_solution.variables, integral_solution.running_time
            )
    lp_solver.clear()


def main():
    load_dotenv()
    create_tables()
    num_processes = int(os.environ.get("NUMBER_OF_PROCESSES"))
    graph_type = os.environ.get("GRAPH_GENERATION_TYPE")
    task_queue = []
    if graph_type == 'random':
        plans = pd.read_csv(
            'random_plan.csv',
            dtype={'min_items': int, 'max_items': int, 'min_players': int, 'max_players': int, 'min_edges': int,
                   'max_edges': int, 'samples': int
                   })

        for index, row in plans.iterrows():
            no_samples = row['samples']
            for i in range(no_samples):
                task_queue.append(RandomBiGraph(
                    row['min_items'],
                    row['max_items'],
                    row['min_players'],
                    row['max_players'],
                    row['min_edges'],
                    row['max_edges']
                ))
    else:
        plans = pd.read_csv('plan.csv', dtype={
            'nodes': int,
            'min_pairs': int,
            'max_pairs': int,
            'samples': int
        })

        for index, row in plans.iterrows():
            no_samples = row['samples']
            for i in range(no_samples):
                task_queue.append(ConsecutiveGraph(row['nodes'], row['min_pairs'], row['max_pairs']))

    with Pool(processes=num_processes) as pool:
        pool.map(process_task, task_queue)


if __name__ == '__main__':
    main()
