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


def discrete_strategy(graph: dict,
                      n_bins: int = 100,
                      starting_node: int = 0
                      ) -> float:
    """
    Discrete strategy to solve the TSP using OR-Tools.
    """
    n_nodes = graph['n_nodes']
    time_range = graph['time_range']
    time_increments = (time_range[1] - time_range[0])/(n_bins - 1)

    # Initialize OR-Tools solver
    solver = pywraplp.Solver.CreateSolver("SCIP")

    # Define a vertex for each pair of nodes and timesteps
    vertices = [{'node': i, 'step': t}
                for i in range(n_nodes) for t in range(n_bins)]

    # Define the objective function
    objective = solver.Objective()
    # Define decision variables and associated costs
    x = dict()
    cost = dict()
    # A variable will represent each edge that connect each pair two vertices
    # (two pairs of nodes and timesteps)
    for vertex1, vertex2 in product(vertices, vertices):
        if vertex1['node'] != vertex2['node']:
            weight_func = graph[(vertex1['node'], vertex2['node'])]
            travel_time = weight_func(vertex1['step'])
            # The number of timesteps that the travel will take
            # At least 1 to avoid loops
            round_travel_timesteps = max(round(travel_time/time_increments),
                                         1)
            if vertex2['step'] - vertex1['step'] == round_travel_timesteps:
                # It is possible to travel from vertex1 to vertex2
                edge = Edge(vertex1["node"], vertex1["step"],
                            vertex2["node"], vertex2["step"])
                x[edge] = solver.BoolVar(
                    f'x_{edge.start_node}_{edge.start_step}' +
                    f'_{edge.end_node}_{edge.end_step}')
                cost[edge] = travel_time
                # objective.SetCoefficient(x[edge], travel_time)

    for node in range(n_nodes):
        # for each node, the sum of the variables representing leaving edges
        # and receiving edges must be one
        receiving_edges = [x[edge] for edge in edges_to_node(node, x)]
        leaving_edges = [x[edge] for edge in edges_from_node(node, x)]
        solver.Add(sum(receiving_edges) == 1)
        solver.Add(sum(leaving_edges) == 1)

        arriving_time = sum([x[edge] * edge.end_step
                             for edge in edges_to_node(node, x)])
        leaving_time = sum([x[edge] * edge.start_step
                            for edge in edges_from_node(node, x)])
        if node != starting_node:
            # The we should leave a node in the same moment we arrive
            solver.Add(arriving_time == leaving_time)
        else:
            # Except for the initial node
            solver.Add(leaving_time <= arriving_time)
            for edge in edges_to_node(node, x):
                objective.SetCoefficient(x[edge], edge.end_step)

    objective.SetMinimization()

    print("Starting solver...")

    # Find the solution
    solver.Solve()

    print("Solver finished.")

    # Print all edges that are 1 in the solution
    for edge in x.keys():
        if x[edge].solution_value() == 1:
            print(f"Edge {edge} is in the solution.")

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
        print(f"step {next_edge.start_step} -> {next_edge.end_step}")
        print(f"solution: {solution}")
    # return the solution
    return solution


def edges_from_node(node, x):
    return [edge for edge in x.keys() if edge.start_node == node]


def edges_to_node(node, x):
    return [edge for edge in x.keys() if edge.end_node == node]


if __name__ == "__main__":
    from trafficTSP.CreateProblems.graphs import create_graph
    graph = create_graph(n_nodes=4)
    discrete_strategy(graph)
    # Expected output: [0, 3, 2, 1]
