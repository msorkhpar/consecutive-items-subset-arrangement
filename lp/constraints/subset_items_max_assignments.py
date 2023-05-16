import logging

from lp.parameters import Parameters

logger = logging.getLogger(__name__)


def set_max_k_total_value_picked_subset_items(parameters: Parameters):
    for i, _ in parameters.items():
        constraint = parameters.add_range_constraint(0, 1, f"sum of neighbors of Item({i}) <= 1")
        string = ""
        for j in parameters.neighbors(i):
            string += f"{parameters.variable(i, j)}+"
            constraint.SetCoefficient(parameters.variable(i, j), 1)

        logger.debug(f"sum({string[:-1]}) <= 1")
