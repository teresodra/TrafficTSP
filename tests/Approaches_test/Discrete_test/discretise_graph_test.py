import pytest
import pandas as pd
import random
from trafficTSP.CreateProblems.graphs import create_graph
from trafficTSP.Approaches.Discrete.discretise_graph import (
    discretise_and_approximate_graph
)

# Fixed seed for reproducibility
random.seed(42)


@pytest.fixture
def fixed_graph_2():
    """Creates a fixed random graph using a deterministic seed."""
    random.seed(42)
    return create_graph(n_nodes=2)


@pytest.fixture
def fixed_graph_4():
    """Creates a fixed random graph using a deterministic seed."""
    random.seed(42)
    return create_graph(n_nodes=4)


def test_discretise_and_approximate_graph_2_nodes(fixed_graph_2):
    """Testing the discretisation function with a 2-node graph"""
    result = discretise_and_approximate_graph(fixed_graph_2, bins=5)

    # Assert the result is a DataFrame
    assert isinstance(result, pd.DataFrame), (
        "Result should be a DataFrame."
    )

    # Check that the DataFrame contains the expected columns
    expected_columns = ['start_node', 'final_node', 'time', 'travel_time']
    assert list(result.columns) == expected_columns, (
        f"Expected {expected_columns} columns, but got {list(result.columns)}."
    )

    # Check for NaN values (there shouldn't be any)
    assert not result['travel_time'].isnull().any(), (
        "There are NaN values in the 'travel_time' column."
    )

    # Check the number of rows (should be n_nodes * (n_nodes - 1) * bins)
    expected_rows = (2 * (2 - 1) * 5)  # 2 nodes, 1 edge per pair, 5 time bins
    assert len(result) == expected_rows, (
        f"The number of rows should be {expected_rows}, but got {len(result)}."
    )


def test_discretise_and_approximate_graph_1_node():
    """With 1 node (no edges, empty DataFrame expected)"""
    graph = create_graph(1)
    result = discretise_and_approximate_graph(graph, bins=5)

    # Assert that the DataFrame is empty
    # as there are no edges in a 1-node graph
    assert result.empty, (
        "The DataFrame should be empty when there is only 1 node."
    )


def test_discretise_and_approximate_graph_1_bin(fixed_graph_4):
    """With bins = 1 (edge case). All values are 0 or 1"""
    result = discretise_and_approximate_graph(fixed_graph_4, bins=1)

    # Check that the result DataFrame is not empty
    # and contains the expected single time step (bins = 1)
    assert not result.empty, (
        "The DataFrame should not be empty."
    )

    # Check if all weights are 0 or 1
    assert all(result['travel_time'].isin([0, 1])), (
        "All weights should be 0 or 1."
    )


def test_discretise_and_approximate_graph_rounding(fixed_graph_4):
    """Check if the costs are integer values after rounding"""
    result = discretise_and_approximate_graph(fixed_graph_4, bins=5)

    # Check if all values in the 'travel_time' column are rounded integers
    assert all(result['travel_time'].apply(lambda x: isinstance(x, int))), (
        "All values in 'travel_time' column should be integers after rounding."
    )


if __name__ == "__main__":
    pytest.main()
