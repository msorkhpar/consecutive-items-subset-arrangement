from __future__ import annotations

import numpy as np

from lp.parameters import Parameters
import logging

logger = logging.getLogger(__name__)


def from_index(index: str) -> tuple[str, str]:
    i, j = index[2:-1].split(",")
    return i, j


class Solution:

    def __init__(self):
        self.K: float | None = None
        self.variables: dict[tuple[str, str], float] = dict()
        self.running_time: float | None = None

    def assign_solution(self, parameter: Parameters):
        self.K = np.round(parameter.variables.get('K', 0).solution_value(), 5)
        target_variables = {from_index(variable): value.solution_value() for variable, value in
                            parameter.variables.items() if variable != 'K'}
        target_variables = dict(sorted(target_variables.items(), key=lambda x: x[1], reverse=True))
        self.variables = target_variables.copy()

