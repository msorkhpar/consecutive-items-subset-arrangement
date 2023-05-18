from __future__ import annotations

import time

import networkx as nx
from ortools.linear_solver import pywraplp

from lp.parameters import Parameters
from lp.solution import Solution
from lp.variables.adjacency_variables import create_adjacency_variables
from lp.constraints.player_omit_infeasible_small_neighbors import omit_infeasible_neighbors
from lp.constraints.player_satisfaction import set_min_k_total_value_assigned_to_player
from lp.constraints.subset_items_max_assignments import set_max_k_total_value_picked_subset_items
from lp.objectives.maximize_k import maximize_k


class Solver:
    def __init__(self, graph: nx.Graph):
        self._graph = graph
        self.parameters = Parameters(self._graph)
        self._create_variables()
        self._set_up_constraints()
        self._set_objectives()

    def _create_variables(self):
        create_adjacency_variables(self.parameters)

    def _set_up_constraints(self):
        set_max_k_total_value_picked_subset_items(self.parameters)
        set_min_k_total_value_assigned_to_player(self.parameters)
        omit_infeasible_neighbors(self.parameters)

    def _set_objectives(self):
        maximize_k(self.parameters)

    def change_to_integral(self):
        self.parameters.change_to_integral()

    def solve(self) -> Solution | None:
        start = time.time()
        status = self.parameters.solve()
        if status == pywraplp.Solver.OPTIMAL:
            solution = Solution()
            solution.running_time = time.time() - start
            solution.assign_solution(self.parameters)
            return solution

        return None

    def clear(self):
        self.parameters.clear_context()
        del self.parameters
