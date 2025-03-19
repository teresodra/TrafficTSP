"""
In this file we will implement a strategy that will solve the problem as a TSP.
But each node will be associated to multiple vertices, once for each timestep.
Instead of passing once through each node, we pass by one of its vertices.
"""
from itertools import product
from collections import namedtuple
from trafficTSP.Approaches.DiscreteWithGraph.discretise_graph import (
    discretise_and_approximate_graph
)
from ortools.linear_solver import pywraplp

# Define Edge as a named tuple to improve readability
Edge = namedtuple('Edge', ['start_node', 'start_step', 'end_node', 'end_step'])


def discrete_strategy(graph: dict,
                      n_bins: int = 50,
                      starting_node: int = 0
                      ) -> float:
    """
    Discrete strategy to solve the TSP using OR-Tools.
    """
    n_nodes = graph['n_nodes']
    # Discretize the graph
    graph_df = discretise_and_approximate_graph(graph, n_bins)

    # Initialize OR-Tools solver
    solver = pywraplp.Solver.CreateSolver("SCIP")

    # Define a vertex for each pair of nodes and timesteps
    vertices = [{'node': i, 'step': t}
                for i in range(n_nodes) for t in range(n_bins)]

    # Define decision variables and associated costs
    x = {}
    cost = {}
    # A variable will represent each edge that connect each pair two vertices
    # (two pairs of nodes and timesteps)
    for vertex1, vertex2 in product(vertices, vertices):
        if vertex1['node'] != vertex2['node']:
            travel_time = graph_df.loc[
                (graph_df['start_node'] == vertex1['node']) &
                (graph_df['final_node'] == vertex2['node']) &
                (graph_df['time'] == vertex1['step']),
                'travel_time'
            ].values[0]
            if vertex2['step'] - vertex1['step'] > travel_time:
                # It is possible to travel from vertex1 to vertex2
                edge = Edge(vertex1["node"], vertex1["step"],
                            vertex2["node"], vertex2["step"])
                x[edge] = solver.BoolVar(
                    f'x_{vertex1["node"]}_{vertex1["step"]}' +
                    '_{vertex2["node"]}_{vertex2["step"]}')
                cost[edge] = vertex2['step'] - vertex1['step']

    for node in range(n_nodes):
        # for each node, the sum of the variables representing leaving edges
        # and receiving edges must be one
        receiving_edges = [x[edge] for edge in edges_to_node(node, x)]
        leaving_edges = [x[edge] for edge in edges_from_node(node, x)]
        solver.Add(sum(receiving_edges) == 1)
        solver.Add(sum(leaving_edges) == 1)

        receiving_time = sum([x[edge] * edge.end_step
                              for edge in edges_to_node(node, x)])
        leaving_time = sum([x[edge] * edge.start_step
                            for edge in edges_from_node(node, x)])
        if node != starting_node:
            # The we should leave a node only after arriving
            solver.Add(receiving_time <= leaving_time)
        else:
            # Except for the initial node
            solver.Add(leaving_time <= receiving_time)
            # Minimise the time of returning to the starting node
            objective = solver.Objective()
            objective.SetMinimization()

    # Find the solution
    solver.Solve()

    # Organize the solution as a list of nodes
    solution = [starting_node]
    while len(solution) < n_nodes:
        current_node = solution[-1]
        next_edge = [
            edge for edge in edges_from_node(current_node, x)
            if x[edge].solution_value() == 1
            ][0]
        next_node = next_edge.end_node
        solution.append(next_node)
    # return the cost of the solution
    return objective.Value()


def edges_from_node(node, x):
    return [edge for edge in x.keys() if edge.start_node == node]


def edges_to_node(node, x):
    return [edge for edge in x.keys() if edge.end_node == node]


if __name__ == "__main__":
    from trafficTSP.CreateProblems.graphs import create_graph
    graph = create_graph(n_nodes=4)
    discrete_strategy(graph)
    # Expected output: [0, 3, 2, 1]
