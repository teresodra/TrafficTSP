from itertools import product
from collections import namedtuple
from ortools.sat.python import cp_model
from trafficTSP.Approaches.Greedy.greedy_strategy import GreedyStrategy

Edge = namedtuple('Edge', ['start_node', 'start_step', 'end_node', 'end_step'])


class DiscreteStrategy:
    def __init__(self, graph: dict,
                 n_bins: int = 30,
                 starting_node: int = 0,
                 time_range: tuple = None,
                 relative_gap_limit: float = 0.05
                 ):
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

        self.vertices = [{'node': i, 'step': t} for i in range(self.n_nodes)
                         for t in range(n_bins)]
        # Stop solving when being this close to the solution
        self.relative_gap_limit = relative_gap_limit

        self.model = cp_model.CpModel()
        self.edge_vars = {}
        self.travel_times = {}

        self.define_variables()
        self.define_constraints()

    def define_variables(self):
        for vertex1, vertex2 in product(self.vertices, self.vertices):
            if vertex1['node'] != vertex2['node']:
                weight_func = self.graph[(vertex1['node'], vertex2['node'])]
                travel_time = weight_func(vertex1['step'])
                round_travel_timesteps = max(
                    1, round(travel_time / self.time_increments)
                )

                if vertex2['step'] - vertex1['step'] == round_travel_timesteps:
                    edge = Edge(vertex1["node"], vertex1["step"],
                                vertex2["node"], vertex2["step"])
                    var = self.model.NewBoolVar(
                        f'x_{edge.start_node}_{edge.start_step}' +
                        f'_{edge.end_node}_{edge.end_step}')
                    self.edge_vars[edge] = var
                    self.travel_times[edge] = travel_time

    def define_constraints(self):
        for node in range(self.n_nodes):
            receiving_edges = [self.edge_vars[edge]
                               for edge in self.edges_to_node(node)]
            leaving_edges = [self.edge_vars[edge]
                             for edge in self.edges_from_node(node)]

            self.model.Add(sum(receiving_edges) == 1)
            self.model.Add(sum(leaving_edges) == 1)

            arriving_time = sum(self.edge_vars[edge] * edge.end_step
                                for edge in self.edges_to_node(node))
            leaving_time = sum(self.edge_vars[edge] * edge.start_step
                               for edge in self.edges_from_node(node))

            if node != self.starting_node:
                self.model.Add(arriving_time == leaving_time)
            else:
                self.model.Add(leaving_time == 0)

        # Objective: minimize total travel time
        self.model.Minimize(
            sum(self.edge_vars[edge] * int(self.travel_times[edge])
                for edge in self.edge_vars)
        )

    def solve(self):
        solver = cp_model.CpSolver()
        solver.parameters.relative_gap_limit = self.relative_gap_limit
        # Stop if within 95% of optimal
        solver.parameters.max_time_in_seconds = 60.0

        print("Starting CP-SAT solver...")
        status = solver.Solve(self.model)
        print("Solver finished with status:", solver.StatusName(status))

        if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            greedy_strategy = GreedyStrategy(self.graph)
            return greedy_strategy.solve()

        # Extract solution path
        solution = [self.starting_node]
        while len(solution) < self.n_nodes:
            current_node = solution[-1]
            edges = self.edges_from_node(current_node)
            for edge in edges:
                if solver.BooleanValue(self.edge_vars[edge]):
                    next_node = edge.end_node
                    print(f"step {edge.start_step} -> {edge.end_step}")
                    solution.append(next_node)
                    break

        return solution

    def edges_from_node(self, node):
        return [edge for edge in self.edge_vars if edge.start_node == node]

    def edges_to_node(self, node):
        return [edge for edge in self.edge_vars if edge.end_node == node]


if __name__ == "__main__":
    from trafficTSP.CreateProblems.graphs import create_graph

    graph = create_graph(n_nodes=4)
    tsp_solver = DiscreteStrategy(graph)
    solution = tsp_solver.solve()
    print("Final solution:", solution)
