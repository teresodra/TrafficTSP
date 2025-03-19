import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from sqlalchemy import create_engine
from trafficTSP.CreateProblems.graphs import create_graph
from trafficTSP.Compare.evaluate_strategy import evaluate_strategy
from trafficTSP.Approaches.Greedy.greedy_strategy import greedy_strategy

default_db_location = "databases\\strategy_results.db"


def compare_strategies(strategies: dict,
                       max_nodes: str = 10,
                       n_repetitions: int = 5):
    """
    Compare the strategies in randomly generated graphs.
    """
    results = []
    for n_nodes in range(3, max_nodes):
        print(f"Running for {n_nodes} nodes")
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

    # Visualise results
    name = "results"
    for key in strategies.keys():
        name += "_" + key
    name += f"_nodes_{max_nodes}_reps_{n_repetitions}.png"
    visualise_results(name)


def save_results_to_sql(results, db_name=default_db_location):
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


def visualise_results(name: str = "results.png",
                      db_name: str = default_db_location):
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
    fig, ax1 = plt.subplots()

    # Create a second y-axis
    ax2 = ax1.twinx()

    # Number of unique strategies
    strategies = df["strategy"].unique()

    # Generate a list of colors from the 'viridis' colormap
    colours = plt.cm.viridis(np.linspace(0, 1, len(strategies)))

    # Loop through strategies and plot
    for strategy, colour in zip(strategies, colours):
        data = df[df["strategy"] == strategy]

        # Solid line for cost
        ax1.plot(data["n_nodes"], data["avg_cost"],
                 color=colour, label=f"{strategy} - Cost",
                 linestyle="-")

        # Dotted line for time taken
        ax2.plot(data["n_nodes"], data["avg_time"],
                 color=colour, label=f"{strategy} - Time Taken",
                 linestyle="dotted")

    # Labels and titles
    ax1.set_xlabel("Number of Nodes")
    ax1.set_ylabel("Cost (Minutes)")
    ax2.set_ylabel("Time Taken (Seconds)")

    # Title
    plt.title("Strategy Performance Comparison")

    # Legends
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Save the plot
    plt.savefig(f"results\\{name}.png")

    # Show the plot
    plt.show()


if __name__ == "__main__":
    strategies = {
        "Greedy": greedy_strategy
    }
    compare_strategies(strategies, max_nodes=10, n_repetitions=5)
