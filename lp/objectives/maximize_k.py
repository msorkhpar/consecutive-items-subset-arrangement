from lp.parameters import Parameters


def maximize_k(parameter: Parameters):
    parameter.maximize(parameter.get_k())
