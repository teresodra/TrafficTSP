from trafficTSP.Compare.compare_strategies import compare_strategies
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy
from trafficTSP.Approaches.Random.random_strategy import random_strategy
import argparse


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
            "Random": random_strategy
        },
        max_nodes=args.nodes,
        n_repetitions=10
    )


if __name__ == "__main__":
    main()
