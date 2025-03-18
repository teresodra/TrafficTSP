import random
import math
from trafficTSP.CreateProblems.weight_functions import (
    create_random_weight_function
)


def create_graph(n_nodes: int,
                 max_distance: float = 10,
                 time_range: tuple[float, float] = (0, 480)
                 ) -> dict:
    """
    Returns a graph saved in a dictionary
    with n_nodes and weight functions for the edges.
    """
    # Create n_nodes nodes with random locations
    # in a square in which max_distance is the desired
    side = max_distance/math.sqrt(2)
    nodes = [(random.uniform(0, side), random.uniform(0, side))
             for _ in range(n_nodes)]

    # Create a graph with random weight functions
    graph = {
        'n_nodes': n_nodes,
        'time_range': time_range
        }
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                graph[(i, j)] = create_random_weight_function(
                    nodes[i],
                    nodes[j],
                    mean_range=time_range
                )
    return graph
