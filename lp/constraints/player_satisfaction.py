import logging

from lp.parameters import Parameters

logger = logging.getLogger(__name__)


def set_min_k_total_value_assigned_to_player(parameters: Parameters):
    for j in parameters.players():
        constraint = parameters.add_range_constraint(0, parameters.infinity(), f"sum of N[P({j})] * V_Ni -K >=0")
        string = ""
        for i in parameters.neighbors(j):
            string += f"{parameters.value(i)} {parameters.variable(i, j)}+"
            constraint.SetCoefficient(parameters.variable(i, j), parameters.value(i))

        constraint.SetCoefficient(parameters.get_k(), -1)
        logger.debug(f"sum({string[:-1]}) - K >= 0 ")
