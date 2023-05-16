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

    def solve(self) -> Solution or None:
        parameter = Parameters(self._graph)
        try:
            create_adjacency_variables(parameter)
            set_max_k_total_value_picked_subset_items(parameter)
            set_min_k_total_value_assigned_to_player(parameter)
            omit_infeasible_neighbors(parameter)
            maximize_k(parameter)
            status = parameter.solve()
            if status == pywraplp.Solver.OPTIMAL:
                solution = Solution()
                solution.assign_solution(parameter)
                if solution.fractional_k == 1.0:
                    parameter.change_to_integral()
                    status = parameter.solve()
                    if status == pywraplp.Solver.OPTIMAL:
                        solution.assign_solution(parameter)
                return solution
        finally:
            parameter.clear_context()
            del parameter
        return None
