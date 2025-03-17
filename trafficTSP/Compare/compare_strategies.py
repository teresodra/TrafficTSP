import matplotlib.pyplot as plt
import pandas as pd
import time
from sqlalchemy import create_engine
from trafficTSP.CreateProblems.graphs import create_graph
from trafficTSP.Compare.evaluate_strategy import evaluate_strategy
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy


def compare_strategies(strategies: dict,
                       max_nodes: str = 100,
                       n_repetitions: int = 10):
    """
    Compare the strategies in the list with the given data.
    """
    results = []
    for n_nodes in range(3, max_nodes):
        # run n_repetitions
        for _ in range(n_repetitions):
            graph = create_graph(n_nodes)
            for strategy_name, strategy in strategies.items():
                start_time = time.time()
                # Cost of the solution
                cost = evaluate_strategy(graph, strategy)
                end_time = time.time()
                # Time to find the solution
                time_taken = end_time - start_time

                # Append results to list
                results.append({
                    "strategy": strategy_name,
                    "n_nodes": n_nodes,
                    "cost": cost,
                    "time_taken": time_taken
                })

    # Save to SQL
    save_results_to_sql(results)

    visualise_results(max_nodes=max_nodes)


def save_results_to_sql(results, db_name="strategy_results.db"):
    """
    Save the Pandas DataFrame results to an SQLite database.
    """
    # Convert to DataFrame
    df_results = pd.DataFrame(results)
    # Connect to SQLite DB
    engine = create_engine(f"sqlite:///{db_name}")
    # Save to SQL
    df_results.to_sql("results", con=engine, if_exists="replace", index=False)
    print(f"✅ Results saved to {db_name}")


def visualise_results(max_nodes,
                      db_name="strategy_results.db"):
    """
    Visualise strategy performance:
    - Solid line: Average cost per strategy
    - Dotted line: Average time taken per strategy
    """
    # Connect to the database and load results
    engine = create_engine(f"sqlite:///{db_name}")
    query = """
        SELECT strategy, n_nodes,
               AVG(cost) AS avg_cost,
               AVG(time_taken) AS avg_time
        FROM results
        GROUP BY strategy, n_nodes
    """
    df = pd.read_sql(query, con=engine)

    # Create a plot
    plt.figure()

    # Loop through strategies and plot
    for strategy in df["strategy"].unique():
        data = df[df["strategy"] == strategy]

        # Solid line for cost
        plt.plot(data["n_nodes"], data["avg_cost"],
                 color='blue', label=f"{strategy} - Cost", linestyle="-")

        # Dotted line for time taken
        plt.plot(data["n_nodes"], data["avg_time"],
                 color='blue', label=f"{strategy} - Time", linestyle="dotted")

    # Labels and title
    plt.xlabel("Number of Nodes")
    plt.ylabel("Cost / Time (s)")
    plt.title("Strategy Performance Comparison")
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    strategies = {
        "Greedy": greedy_strategy
    }
    compare_strategies(strategies, max_nodes=30, n_repetitions=5)
