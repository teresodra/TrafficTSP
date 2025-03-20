"""
In this file we will implement a strategy that will solve the problem as a TSP.
But each node will be associated to multiple vertices, once for each timestep.
Instead of passing once through each node, we pass by one of its vertices.
"""
from itertools import product
from collections import namedtuple
# from trafficTSP.Approaches.DiscreteWithGraph.discretise_graph import (
#     discretise_and_approximate_graph
# )
from ortools.linear_solver import pywraplp

# Define Edge as a named tuple to improve readability
Edge = namedtuple('Edge', ['start_node', 'start_step', 'end_node', 'end_step'])


class DiscreteStrategy:
    """
    Discrete strategy to solve the TSP using OR-Tools.
    """
    def __init__(self,
                 graph: dict,
                 n_bins: int = 40,
                 starting_node: int = 0,
                 time_range: tuple = None
                 ) -> float:

        self.graph = graph
        self.n_bins = n_bins
        self.starting_node = starting_node
        self.n_nodes = graph['n_nodes']
        if time_range is None:
            self.time_range = graph['time_range']
        else:
            self.time_range = time_range
        self.time_increments = ((self.time_range[1] - self.time_range[0]) /
                                (n_bins - 1))

        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        self.vertices = [{'node': i, 'step': t} for i in range(self.n_nodes)
                         for t in range(n_bins)]
        self.x = {}
        self.objective = self.solver.Objective()

    def define_variables(self):
        """Define decision variables and influence in the objective."""
        for vertex1, vertex2 in product(self.vertices, self.vertices):
            if vertex1['node'] != vertex2['node']:
                weight_func = self.graph[(vertex1['node'], vertex2['node'])]
                travel_time = weight_func(vertex1['step'])
                round_travel_timesteps = max(
                    1, round(travel_time / self.time_increments),
                    )

                if vertex2['step'] - vertex1['step'] == round_travel_timesteps:
                    edge = Edge(vertex1["node"], vertex1["step"],
                                vertex2["node"], vertex2["step"])
                    self.x[edge] = self.solver.BoolVar(
                        f'x_{edge.start_node}_{edge.start_step}_' +
                        f'{edge.end_node}_{edge.end_step}'
                        )
                    self.objective.SetCoefficient(self.x[edge], travel_time)

    def define_constraints(self):
        """Define flow constraints to ensure valid paths."""
        for node in range(self.n_nodes):
            receiving_edges = [self.x[edge]
                               for edge in self.edges_to_node(node)]
            leaving_edges = [self.x[edge]
                             for edge in self.edges_from_node(node)]
            self.solver.Add(sum(receiving_edges) == 1)
            self.solver.Add(sum(leaving_edges) == 1)

            arriving_time = sum([self.x[edge] * edge.end_step
                                 for edge in self.edges_to_node(node)])
            leaving_time = sum([self.x[edge] * edge.start_step
                                for edge in self.edges_from_node(node)])

            if node != self.starting_node:
                self.solver.Add(arriving_time == leaving_time)
            else:
                self.solver.Add(leaving_time == 0)

        self.objective.SetMinimization()

    def solve(self):
        """Solve the TSP problem and return the optimal path."""
        print("Starting solver...")
        self.solver.Solve()
        print("Solver finished.")

        for edge in self.x.keys():
            if self.x[edge].solution_value() == 1:
                print(f"Edge {edge} is in the solution.")

        solution = [self.starting_node]
        while len(solution) < self.n_nodes:
            current_node = solution[-1]
            next_edge = [edge for edge in self.edges_from_node(current_node)
                         if self.x[edge].solution_value() == 1][0]
            next_node = next_edge.end_node
            solution.append(next_node)
            print(f"step {next_edge.start_step} -> {next_edge.end_step}")
            print(f"solution: {solution}")

        return solution

    def edges_from_node(self, node):
        return [edge for edge in self.x.keys() if edge.start_node == node]

    def edges_to_node(self, node):
        return [edge for edge in self.x.keys() if edge.end_node == node]


if __name__ == "__main__":
    from trafficTSP.CreateProblems.graphs import create_graph
    graph = create_graph(n_nodes=4)
    tsp_solver = DiscreteStrategy(graph)
    tsp_solver.define_variables()
    tsp_solver.define_constraints()
    solution = tsp_solver.solve()
    print("Final solution:", solution)
