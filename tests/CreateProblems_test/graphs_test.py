from trafficTSP.CreateProblems.graphs import create_graph


def test_create_graph_structure():
    """Ensure create_graph generates the correct graph structure."""
    n_nodes = 5
    graph = create_graph(n_nodes)

    # Expected number of edges: n_nodes * (n_nodes - 1)
    expected_edges = n_nodes * (n_nodes - 1)
    edges = {key: value for key, value in graph.items()
             if isinstance(key, tuple)}
    real_edges = len(edges)
    assert real_edges == expected_edges, (
        "Incorrect number of edges in the graph"
    )

    # Check that all edges have callable weight functions
    for edge, weight_fn in edges.items():
        assert isinstance(edge, tuple) and len(edge) == 2, (
                "Edge keys must be tuples (i, j)"
            )
        assert callable(weight_fn), (
                "Weight function must be callable"
            )


def test_weight_function_returns_number():
    """Ensure the weight function returns a valid number."""
    graph = create_graph(n_nodes=3)

    edges = {key: value for key, value in graph.items()
             if isinstance(key, tuple)}

    for weight_fn in edges.values():
        weight_value = weight_fn(0)  # Call the function with t=0

        assert isinstance(weight_value, float), (
                "Weight function must return a number"
        )
        assert weight_value >= 0, (
                "Weight value should not be negative"
        )


def test_empty_graph():
    """Ensure an empty graph is returned when n_nodes is 0."""
    time_range = (0, 480)
    graph = create_graph(0, time_range=time_range)

    assert graph == {'n_nodes': 0, 'time_range': time_range}, (
        "Graph should be empty when there are no nodes"
    )
