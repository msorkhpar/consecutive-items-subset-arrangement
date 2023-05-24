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
class InputData:
    nodes: int
    min_pairs: int
    max_pairs: int
    mode: str = "consecutive"


def process_task(input_data: InputData):
    if input_data == "consecutive":
        items, players, item_sets, edges = generate_random_consecutive_items_edge_set(
            input_data.nodes, input_data.min_pairs, input_data.max_pairs
        )
        G = construct_bipartite_graph(items, players, edges)
        logger.info(f"A sample with {len(items)} items, {len(players)} players, and {len(edges)} edges is created.")
    else:
        G = generate_random_edge_set(input_data.nodes, input_data.min_pairs, input_data.max_pairs)
        logger.info(f"A sample random graph {G}] is created. ")

    assign_random_values_to_item_set(G)
    ceiling_big_item_values(G)
    bigraph_id = persist_bigraph(G)

    lp_solver = Solver(G)
    solution = lp_solver.solve()
    if solution is None:
        return
    persist_fractional_solution(bigraph_id, solution.K, solution.variables, solution.running_time)
    logger.info(f"Fractional K=[{solution.K}] for sample[{bigraph_id}] has been found.")
    if solution.K == 1.0:
        lp_solver.change_to_integral()
        solution = lp_solver.solve()
        if solution is None:
            return
        persist_integral_solution(bigraph_id, solution.K, solution.variables, solution.running_time)
        logger.info(f"Integral K=[{solution.K}] for sample[{bigraph_id}] has been found.")
    lp_solver.clear()


def main():
    load_dotenv()
    create_tables()
    num_processes = int(os.environ.get("NUMBER_OF_PROCESSES"))
    graph_type = os.environ.get("GRAPH_GENERATION_TYPE")
    task_queue = []

    plans = pd.read_csv('plan.csv', dtype={
        'nodes': int,
        'min_pairs': int,
        'max_pairs': int,
        'samples': int
    })

    for index, row in plans.iterrows():
        no_samples = row['samples']
        for i in range(no_samples):
            task_queue.append(InputData(row['nodes'], row['min_pairs'], row['max_pairs'], graph_type))

    with Pool(processes=num_processes) as pool:
        pool.map(process_task, task_queue)


if __name__ == '__main__':
    main()
