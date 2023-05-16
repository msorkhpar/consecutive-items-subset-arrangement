import logging


from lp.parameters import Parameters

logger = logging.getLogger(__name__)


def omit_infeasible_neighbors(parameters: Parameters):
    for j in parameters.players():
        filtered_edges = list()
        total_value = 0
        for i in parameters.neighbors(j):
            value = parameters.value(i)
            if value < 0.5:
                total_value += value
                filtered_edges.append(parameters.variable(i, j))

        if total_value < 1:
            string = f"for P({j}): "
            for variable in filtered_edges:
                string += f"{variable}=0,"
                parameters.add_constraint_rule(variable == 0)
            logger.debug(string[:-1])
