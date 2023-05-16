from lp.solver import Parameters


def create_adjacency_variables(parameters: Parameters):
    for i, j in parameters.edges():
        parameters.add_variable(i, j)
