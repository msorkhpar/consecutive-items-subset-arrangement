import logging
import os

import pandas as pd
from dotenv import load_dotenv

from generators.generate_bipartite_graph import construct_bipartite_graph
from generators.generate_consecutive_items_bipartite_graph import generate_random_edge_set
from transformers.assign_items_random_values import assign_random_values_to_item_set
from transformers.ceiling_big_items_values import ceiling_big_item_values
from lp.solver import Solver
from persistent.db_service import create_tables, persist_bigraph, persist_fractional_solution, persist_integral_solution

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=int(os.getenv('LOG_LEVEL')))
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    load_dotenv()
    create_tables()

    plans = pd.read_csv('plan.csv', dtype={
        'nodes': int,
        'min_pairs': int,
        'max_pairs': int,
        'samples': int
    })

    for index, row in plans.iterrows():
        no_samples = row['samples']
        for i in range(no_samples):
            items, players, item_sets, edges = generate_random_edge_set(
                row['nodes'], row['min_pairs'], row['max_pairs']
            )
            G = construct_bipartite_graph(items, players, edges)
            assign_random_values_to_item_set(G)
            ceiling_big_item_values(G)
            bigraph_id = persist_bigraph(G)
            logger.info(
                f"A sample with {len(items)} items, {len(players)} players, and {len(edges)} edges is created. "
                f"DB id is [{bigraph_id}]"
            )
            lp_solver = Solver(G)
            solution = lp_solver.solve()
            if solution is None:
                continue
            persist_fractional_solution(bigraph_id, solution.K, solution.variables, solution.running_time)
            logger.info(f"Fractional K for sample[{bigraph_id}] has been found.")
            if solution.K == 1.0:
                lp_solver.change_to_integral()
                solution = lp_solver.solve()
                if solution is None:
                    continue
                persist_integral_solution(bigraph_id, solution.K, solution.variables, solution.running_time)
                logger.info(f"Integral K for sample[{bigraph_id}] has been found.")
            lp_solver.clear()
