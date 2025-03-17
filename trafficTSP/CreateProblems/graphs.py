import random
from trafficTSP.CreateProblems.weight_functions import (
    create_random_weight_function
)


def create_graph(n_nodes: int) -> dict:
    """
    Returns a graph saved in a dictionary
    with n_nodes and weight functions for the edges.
    """
    # Create n_nodes nodes with random locations in the unit square
    nodes = [(random.uniform(0, 1), random.uniform(0, 1))
             for _ in range(n_nodes)]

    # Create a graph with random weight functions
    graph = {'n_nodes': n_nodes}
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                graph[(i, j)] = create_random_weight_function(
                    nodes[i], nodes[j]
                )
    return graph
