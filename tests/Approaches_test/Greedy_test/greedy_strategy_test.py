import pytest
import random
from trafficTSP.CreateProblems.graphs import create_graph
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy


def test_greedy_strategy_single_node():
    """Edge case: If there's only one node."""
    graph = create_graph(n_nodes=1)
    solution = greedy_strategy(graph, start_node=0)

    assert solution == [0], (
        "Should return [0]"
    )


@pytest.fixture
def fixed_graph():
    """Creates a fixed random graph using a deterministic seed."""
    random.seed(42)
    return create_graph(n_nodes=4)


def test_greedy_strategy_valid_path(fixed_graph):
    """Check if the greedy strategy returns a valid path."""
    solution = greedy_strategy(fixed_graph)

    assert isinstance(solution, list), "Solution must be a list"
    assert len(solution) == fixed_graph['n_nodes'], (
        "Solution must contain all nodes"
    )
    assert len(set(solution)) == len(solution), (
        "Solution cannot have duplicates"
    )


def test_greedy_strategy_output(fixed_graph):
    """Check if the greedy strategy returns the right answer."""
    solution = greedy_strategy(fixed_graph)

    assert solution == [0, 3, 1, 2], (
        "The solution should be "
    )
