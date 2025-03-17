import pytest
from trafficTSP.CreateProblems.weight_functions import (
    gaussian,
    create_random_weight_function
)

# ---- Test Gaussian Function ---- #


def test_gaussian_peak():
    """Ensure the Gaussian function has its peak at the mean."""
    mean = 0
    maximum = 1
    assert pytest.approx(gaussian(mean, mean, maximum)) == maximum


def test_gaussian_symmetry():
    """Ensure the Gaussian function is symmetric around the mean."""
    mean = 0
    maximum = 1
    assert (pytest.approx(gaussian(mean - 1, mean, maximum))
            == gaussian(mean + 1, mean, maximum))


def test_gaussian_decreasing():
    """Ensure Gaussian function decreases as we move away from the mean."""
    mean = 0
    maximum = 1
    assert (gaussian(mean, mean, maximum)
            > gaussian(mean + 1, mean, maximum))
    assert (gaussian(mean, mean, maximum)
            > gaussian(mean - 1, mean, maximum))
    assert (gaussian(mean + 1, mean, maximum)
            > gaussian(mean + 2, mean, maximum))
    assert (gaussian(mean - 1, mean, maximum)
            > gaussian(mean - 2, mean, maximum))


# ---- Test Weight Function ---- #


def test_weight_function_basic():
    """Ensure weight function returns reasonable values."""
    initial_node = (0, 0)
    final_node = (3, 4)  # Distance is 5
    weight_function = create_random_weight_function(
        initial_node,
        final_node, maximum_range=(0, 2),
        n_disruptions=1
    )

    weight_at_0 = weight_function(0)
    # Weight should be at least the distance
    assert weight_at_0 >= 5
    # Should not exceed the maximum with one disruption
    assert weight_at_0 < 15
