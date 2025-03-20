from trafficTSP.Compare.compare_strategies import compare_strategies
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy
from trafficTSP.Approaches.Random.random_strategy import random_strategy
from trafficTSP.Approaches.DiscreteWithGraph.discrete_strategy import (
    discrete_strategy
)
import argparse
import random
import time


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', type=int,
                        help='Number of nodes')
    args = parser.parse_args()

    # Compare strategies
    compare_strategies(
        strategies={
            "Greedy": greedy_strategy,
            "Random": random_strategy,
            "Discrete": discrete_strategy
        },
        max_nodes=args.nodes,
        n_repetitions=2
    )


if __name__ == "__main__":
    # Fix the seed for reproducibility
    random.seed(0)
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds.")
