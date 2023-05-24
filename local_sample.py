import logging
import os
from dataclasses import dataclass
from multiprocessing import Lock, Process, Queue

import networkx as nx
import pandas as pd
from dotenv import load_dotenv

from generators.generate_bipartite_graph import construct_bipartite_graph
from generators.generate_consecutive_items_bipartite_graph import generate_random_consecutive_items_edge_set
from transformers.assign_items_random_values import assign_random_values_to_item_set
from transformers.ceiling_big_items_values import ceiling_big_item_values
from lp.solver import Solver
from persistent.db_service import create_tables, persist_bigraph, persist_fractional_solution, persist_integral_solution

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=int(os.getenv('LOG_LEVEL')))
logger = logging.getLogger(__name__)


def process_task(items, players, edges, values):
    G = construct_bipartite_graph(items, players, edges, values)
    lp_solver = Solver(G)
    fractional_solution = lp_solver.solve()
    if fractional_solution is None:
        logger.info("LP could not find a fractional solution.")
        return
    logger.info(f"Fractional K is [{fractional_solution.K}].")
    if fractional_solution.K == 1.0:
        lp_solver.change_to_integral()
        integral_solution = lp_solver.solve()
        if integral_solution is None:
            return
        logger.info(f"Integral K is [{integral_solution.K}]")
        logger.info(f"Fractional variables:")
        logger.info(fractional_solution.variables)

        logger.info(f"Integral variables:")
        logger.info(integral_solution.variables)
    else:
        logger.info("LP could not find an integral solution.")
    lp_solver.clear()


def main():
    load_dotenv()
    example = os.getenv("EXAMPLE")
    values = list()
    items = list()
    players = set()
    edges = list()
    with open(f'examples/{example}-w.txt') as f:
        for line in f:
            item, value = (part.strip() for part in line.split(","))
            items.append(item)
            if "/" in value:
                numerator, denominator = map(int, value.split('/'))
                values.append(round(numerator / denominator, 15))
            else:
                values.append(float(value))

    with open(f'examples/{example}-e.txt') as f:
        for line in f:
            input_data = line.strip().split(",")
            item = input_data[0].strip()
            players.update(input_data[1:])
            edges.extend((item, player) for player in input_data[1:])

    process_task(items, players, edges, values)


if __name__ == '__main__':
    main()
