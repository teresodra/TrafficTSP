import numpy as np
import pytest
import random
from trafficTSP.CreateProblems.graphs import create_graph
from trafficTSP.Compare.evaluate_strategy import (
    evaluate_solution,
    evaluate_strategy
)
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy


@pytest.fixture
def fixed_graph():
    """Creates a fixed random graph for testing."""
    random.seed(42)  # Fix the seed for reproducibility
    return create_graph(n_nodes=4)


# ---- Test Evaluate Solution ---- #


def test_evaluate_solution(fixed_graph):
    """Ensure evaluate_solution correctly calculates total path weight."""
    solution = [0, 1, 3, 2]  # A valid TSP route

    total_weight = evaluate_solution(fixed_graph, solution)

    assert isinstance(total_weight, float), (
        "Total weight should be a number"
        )
    assert total_weight > 0, (
        "Total weight should be positive"
    )
    assert total_weight == np.float64(16.374273794000544), (
        "Total weight should be 16.374273794000544"
    )


def test_evaluate_solution_single_node():
    """If the solution has only one node, the weight should be zero."""
    graph = create_graph(n_nodes=1)
    solution = [0]  # Only one node, no travel

    total_weight = evaluate_solution(graph, solution)

    assert total_weight == 0, (
        "Total weight should be 0"
    )


# ---- Test Evaluate Strategy ---- #


def test_evaluate_strategy(fixed_graph):
    """Test evaluate_strategy correctly evaluates a strategy's performance."""
    total_weight = evaluate_strategy(fixed_graph, greedy_strategy)

    assert isinstance(total_weight, float), (
        "Total weight should be a number"
        )
    assert total_weight > 0, (
        "Total weight should be positive"
    )
    assert total_weight == np.float64(13.661218871595167), (
        "Total weight should be 13.661218871595167"
    )
