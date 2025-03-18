from trafficTSP.Compare.compare_strategies import compare_strategies
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy
from trafficTSP.Approaches.Random.random_strategy import random_strategy

if __name__ == "__main__":
    # Compare strategies
    compare_strategies(
        strategies={
            "Greedy": greedy_strategy,
            "Random": random_strategy
        },
        max_nodes=35,
        n_repetitions=10
    )
