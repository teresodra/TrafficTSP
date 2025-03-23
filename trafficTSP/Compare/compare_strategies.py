import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from sqlalchemy import create_engine
from trafficTSP.CreateProblems.graphs import create_graph
from trafficTSP.Compare.evaluate_strategy import evaluate_strategy

default_db_location = "databases\\strategy_results.db"


def compare_strategies(strategies: dict,
                       max_nodes: str = 10,
                       n_repetitions: int = 5):
    """
    Compare the strategies in randomly generated graphs.
    """
    results = []
    n_strategies = len(strategies)
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
                if len(results) % n_strategies == 0:
                    print(results[-n_strategies:])
                    print("\n")

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
                      db_name: str = default_db_location,
                      old_strategy: str = "Greedy",
                      new_strategy: str = "Discrete"):
    """
    Visualise strategy performance:
    - Solid line: Average cost per strategy
    - Dotted line: Average time taken per strategy
    """
    # Connect to the database and load results
    engine = create_engine(f"sqlite:///{db_name}")

    # Aggregate results
    query_aggregated = """
        SELECT strategy, n_nodes,
            AVG(cost) AS avg_cost,
            AVG(time_taken) AS avg_time
        FROM results
        GROUP BY strategy, n_nodes
    """
    df_aggregated = pd.read_sql(query_aggregated, con=engine)

    # Save aggregated data to a new table
    df_aggregated.to_sql('avg_results', con=engine,
                         index=False, if_exists='replace')

    # Plot the aggregated data
    plot_aggregated_strategy_data(df_aggregated, name)

    # Compare old and new strategies
    available_strategies = df_aggregated["strategy"].unique()
    if (old_strategy in available_strategies and
       new_strategy in available_strategies):
        plot_improvement_old_to_new(engine, old_strategy, new_strategy)
    else:
        raise Exception(f"{old_strategy} or {new_strategy} not available.")


def plot_aggregated_strategy_data(df: pd.DataFrame, name: str):
    """
    Plot the aggregated data.
    """

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
    plt.savefig(f"results\\{name}")

    # Show the plot
    plt.show()


def plot_improvement_old_to_new(engine, old_strategy, new_strategy):
    """
    Plot the improvement from the old to the new strategy.
    """

    # Compute improvement from old to new
    query_improvement = f"""
        SELECT
            g.n_nodes,
            g.avg_cost AS greedy_cost,
            d.avg_cost AS discrete_cost,
            (g.avg_cost / d.avg_cost - 1) AS improvement
        FROM avg_results AS g
        JOIN avg_results AS d
        ON g.n_nodes = d.n_nodes
        WHERE g.strategy = '{old_strategy}' AND d.strategy = '{new_strategy}'
    """

    df_improvement = pd.read_sql(query_improvement, con=engine)

    fig_name = f"results\\improvement_{old_strategy}_to_{new_strategy}"
    # fig_name += f"_nodes_{max_nodes}_reps_{n_repetitions}.png"

    # Plot the improvement
    plt.plot(df_improvement["n_nodes"], df_improvement["improvement"])
    plt.xlabel("Number of Nodes")
    plt.ylabel("Improvement (%)")
    plt.title(f"Improvement from {old_strategy} to {new_strategy}")
    plt.savefig(f"{fig_name}.png")
    plt.show()
