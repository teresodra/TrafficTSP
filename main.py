from trafficTSP.Compare.compare_strategies import compare_strategies
from trafficTSP.Approaches.Greedy.greedy_strategy import GreedyStrategy
# from trafficTSP.Approaches.Random.random_strategy import RandomStrategy
from trafficTSP.Approaches.Discrete.discrete_strategy import (
    DiscreteStrategy
)
import argparse
import random


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', type=int,
                        help='Number of nodes',
                        default=9)
    parser.add_argument('--n_repetitions', type=int,
                        help='Number of repetitions',
                        default=20)
    args = parser.parse_args()

    # Compare strategies
    compare_strategies(
        strategies={
            "Greedy": GreedyStrategy,
            # "Random": RandomStrategy,
            "Discrete": DiscreteStrategy
        },
        max_nodes=args.nodes,
        n_repetitions=args.n_repetitions
    )


if __name__ == "__main__":
    # Fix the seed for reproducibility
    random.seed(0)
    main()
