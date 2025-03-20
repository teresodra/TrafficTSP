import random


class RandomStrategy:
    def __init__(self, graph: dict, start_node: int = 0):
        """
        Random strategy to solve the TSP.
        """
        self.graph = graph
        self.start_node = start_node
        self.n_nodes = graph['n_nodes']
        self.nodes_left = list(range(self.n_nodes))
        self.nodes_left.remove(self.start_node)

    def solve(self):
        """Solve the TSP problem using a random approach."""
        random.shuffle(self.nodes_left)
        return [self.start_node] + self.nodes_left
