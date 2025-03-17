

def greedy_strategy(graph: dict, start_node: int = 0) -> list:
    """
    Returns a solution to the TSP using the greedy strategy.
    """
    n_nodes = graph['n_nodes']
    nodes_left = set(range(1, n_nodes))
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
    return solution
