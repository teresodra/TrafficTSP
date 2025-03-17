import random
import math
from scipy.stats import norm
from typing import Callable


def gaussian(t: float, mean: float, maximum: float) -> float:
    """
    Returns the value in t of a Gaussian function with a specified mean
    and highest value (maximum).
    """
    # Standard deviation of gaussian for desired maximum
    std_dev = 1 / (maximum * math.sqrt(2 * math.pi))
    return norm.pdf(t, loc=mean, scale=std_dev)


def create_random_weight_function(initial_node: tuple[float, float],
                                  final_node: tuple[float, float],
                                  mean_range: tuple[float, float] = (0, 480),
                                  maximum_range: tuple[float, float] = (0, 2),
                                  n_disruptions: int = 2) -> Callable:
    """"
    Returns a weight function that depends on the time of the day.
    The function simulates the traffic with random disruptions.
    """

    # Choose random disruptions
    maxima = [random.uniform(*maximum_range)
              for _ in range(n_disruptions)]
    means = [random.uniform(*mean_range)
             for _ in range(n_disruptions)]

    def weight_function(t: float) -> float:
        """
        Returns the weight at time t.
        Weight is calculated as the distance between the nodes multiplied by
        a factor that depends on the disruptions at that time of the day.
        """
        weight = math.dist(initial_node, final_node)
        for mean, maximum in zip(means, maxima):
            weight *= (1 + gaussian(t, mean, maximum))
        return weight
    return weight_function
