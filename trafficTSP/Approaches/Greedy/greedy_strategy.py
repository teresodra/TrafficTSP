class GreedyStrategy:
    def __init__(self, graph: dict, start_node: int = 0):
        """
        Greedy strategy to solve the TSP.
        """
        self.graph = graph
        self.start_node = start_node
        self.n_nodes = graph['n_nodes']
        self.nodes_left = set(range(self.n_nodes)) - {self.start_node}
        self.solution = [self.start_node]
        self.current_node = self.start_node
        self.t = 0

    def find_next_node(self):
        """Find the closest node from the current node."""
        return min(self.nodes_left,
                   key=lambda node:
                   self.graph[(self.current_node, node)](self.t))

    def solve(self):
        """Solve the TSP problem using a greedy approach."""
        while self.nodes_left:
            next_node = self.find_next_node()
            weight = self.graph[(self.current_node, next_node)](self.t)
            self.t += weight
            self.nodes_left.remove(next_node)
            self.solution.append(next_node)
            self.current_node = next_node
        return self.solution


if __name__ == "__main__":
    from trafficTSP.CreateProblems.graphs import create_graph
    graph = create_graph(n_nodes=4)
    greedy_solver = GreedyStrategy(graph)
    solution = greedy_solver.solve()
    print("Final solution:", solution)
