import random


def random_strategy(graph: dict, start_node: int = 0) -> list:
    """
    Returns a solution to the TSP using the greedy strategy.
    """
    n_nodes = graph['n_nodes']
    # Create a list of nodes left to visit eliminating the start node
    nodes_left = list(range(n_nodes))
    nodes_left.remove(start_node)
    # Randomize the order of the nodes left
    random.shuffle(nodes_left)
    solution = [start_node] + nodes_left
    return solution
