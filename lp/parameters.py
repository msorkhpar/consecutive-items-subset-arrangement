from __future__ import annotations

from functools import lru_cache

import networkx as nx
from ortools.linear_solver import pywraplp


def to_index(i: str, j: str) -> str:
    return f"X({i},{j})"


class Parameters:
    def __init__(self, h: nx.Graph):
        self.with_fractions = True
        self.H: nx.Graph = h
        self._solver = pywraplp.Solver.CreateSolver('SCIP')
        self.variables: dict[str, pywraplp.Variable] = dict()
        self.variables['K'] = self._solver.NumVar(1, 1, 'K')

    def infinity(self) -> float:
        return self._solver.Infinity()

    def variable(self, i: str, j: str) -> pywraplp.Variable:
        return self.variables[to_index(i, j)]

    def get_k(self) -> pywraplp.Variable:
        return self.variables['K']

    def constraints_num(self) -> int:
        return self._solver.NumConstraints()

    def variables_num(self) -> int:
        return self._solver.NumVariables()

    def add_variable(self, i: str, j: str, lower_bound: float = 0.0, upper_bound: float = 1.0):
        index = to_index(i, j)
        if self.with_fractions:
            self.variables[index] = self._solver.NumVar(lower_bound, upper_bound, index)
        else:
            self.variables[index] = self._solver.IntVar(lower_bound, upper_bound, index)

    def add_range_constraint(self, lower_bound: float, upper_bound: float, name=''):
        return self._solver.Constraint(
            lower_bound,
            upper_bound,
            name
        )

    def maximize(self, variable: pywraplp.Variable):
        self._solver.Maximize(variable)

    def minimize(self, variable: pywraplp.Variable):
        self._solver.Minimize(variable)

    def add_constraint_rule(self, constraint_rule: pywraplp.LinearConstraint):
        self._solver.Add(constraint_rule)

    @lru_cache(maxsize=None)
    def edges(self) -> list[tuple[int | str, int | str]]:
        edges = list()
        for i, j in self.H.edges:
            edges.append((i, j))
        return edges

    @lru_cache(maxsize=None)
    def items(self) -> list[tuple[int | str, dict]]:
        return [(n, attr) for n, attr in self.H.nodes(data=True) if self.H.nodes[n]['bipartite'] == 0]

    def value(self, item: int | str) -> float:
        return self.H.nodes[item]['value']

    @lru_cache(maxsize=None)
    def players(self) -> list[str]:
        return [n for n in self.H.nodes if self.H.nodes[n]['bipartite'] == 1]

    @lru_cache(maxsize=None)
    def neighbors(self, node: int | str) -> list[int | str]:
        return list(self.H.neighbors(node))

    def change_to_integral(self):
        if self.with_fractions:
            self.with_fractions = False
            self.variables['K'].SetBounds(0.0, 1.0)
            [self.variables[key].SetInteger(True) for key in self.variables if key != 'K']

    def solve(self) -> int:
        return self._solver.Solve()

    def clear_context(self):
        self._solver.Clear()
