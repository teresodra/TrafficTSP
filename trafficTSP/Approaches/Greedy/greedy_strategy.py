

def greedy_strategy(graph: dict, start_node: int = 0) -> list:
    """
    Returns a solution to the TSP using the greedy strategy.
    """
    n_nodes = graph['n_nodes']
    # Create a set of nodes left to visit eliminating the start node
    nodes_left = set(range(n_nodes))
    nodes_left.remove(start_node)
    # Set the current node as the start node
    current_node = start_node
    solution = [current_node]
    t = 0
    # While there are nodes left to visit
    while nodes_left != set():
        # Choose closest node
        next_node = min(
            nodes_left,
            key=lambda node: graph[(current_node, node)](t)
        )
        # Update t, nodes_left and solution
        weight = graph[(current_node, next_node)](t)
        t += weight
        nodes_left.remove(next_node)
        solution.append(next_node)
        current_node = next_node
    return solution
