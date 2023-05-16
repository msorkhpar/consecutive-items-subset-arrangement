import numpy as np

from lp.parameters import Parameters
import logging

logger = logging.getLogger(__name__)


def from_index(index: str) -> tuple[str, str]:
    i, j = index[2:-1].split(",")
    return i, j


class Solution:

    def __init__(self):
        self.fractional_variables = None
        self.fractional_k = -1.0
        self.integral_variables = None
        self.integral_k = -1.0
        self.ratio = None

    def assign_solution(self, parameter: Parameters):
        k = np.round(parameter.variables.get('K', 0).solution_value(), 5)
        target_variables = {from_index(variable): value.solution_value() for variable, value in
                            parameter.variables.items() if variable != 'K'}
        target_variables = dict(sorted(target_variables.items(), key=lambda x: x[1], reverse=True))
        if parameter.with_fractions:
            self.fractional_variables = target_variables.copy()
            self.fractional_k = k
        else:
            self.integral_variables = target_variables.copy()
            self.integral_k = k
            self.ratio = self.integral_k / self.fractional_k

    def print_result(self):
        if self.fractional_k == 1.0:
            logger.debug(f"Fractional variables: {self.fractional_variables}")
            logger.debug(f"Integral variables: {self.integral_variables}")
            logger.info(f"Fractional K=[{self.fractional_k}]")
            logger.info(f"Integral K=[{self.integral_k}]")
            logger.info(f"(Integral K / Fractional K)=[{self.ratio}]")
        else:
            logger.debug(f"Fractional variables: {self.fractional_variables}")
            logger.info(f"Fractional result is less than 1! K=[{self.fractional_k}]")
