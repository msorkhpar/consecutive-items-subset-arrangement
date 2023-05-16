import logging
import os

import pandas as pd
from dotenv import load_dotenv

from generators.generate_bipartite_graph import construct_bipartite_graph
from generators.generate_consecutive_items_bipartite_graph import generate_random_edge_set
from transformers.assign_items_random_values import assign_random_values_to_item_set
from transformers.ceiling_big_items_values import ceiling_big_item_values
from lp.solver import Solver

logger = logging.getLogger(__name__)
logger.debug("Hi debug")
logger.info("Hi info")

if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=int(os.getenv('LOG_LEVEL')))
    logger = logging.getLogger(__name__)

    plans = pd.read_csv('plan.csv', dtype={
        'nodes': int,
        'min_pairs': int,
        'max_pairs': int,
        'samples': int
    })
    counter = 0
    found_solution = 0

    for index, row in plans.iterrows():
        no_samples = row['samples']
        for i in range(no_samples):
            counter += 1
            if counter % 100 == 0:
                logger.info(f'{counter} problems has been generated and ' +
                            f'{found_solution} of 100 new ones had a solution!')
                found_solution = 0
            items, players, edges = generate_random_edge_set(row['nodes'], row['min_pairs'], row['max_pairs'])
            G = construct_bipartite_graph(items, players, edges)
            assign_random_values_to_item_set(G)
            ceiling_big_item_values(G)
            lp_solver = Solver(G)
            solution = lp_solver.solve()
            if solution is None:
                continue
            found_solution += 1
            if solution.fractional_k == 1.0 and solution.ratio != 1.0:
                solution.print_result()
