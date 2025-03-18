import pandas as pd
import numpy as np


def discretise_graph(graph: dict, bins: int = 10) -> dict:
    """
    Discretises the graph weights into bins.
    """
    n_nodes = graph['n_nodes']
    time_range = graph['time_range']
    discrete_timestamps = [
        time_range[0] + i*(time_range[1] - time_range[0])/bins
        for i in range(bins+1)]
    discrete_timestamps = np.linspace(time_range[0], time_range[1], num=bins)

    # Create the MultiIndex for the DataFrame
    multi_index = pd.MultiIndex.from_product(
        [range(n_nodes), range(n_nodes), discrete_timestamps],
        names=['start_node', 'final_node', 'time']
    )

    # Initialize the DataFrame
    df = pd.DataFrame(index=multi_index, columns=['cost'])
    # Iterate over all the edges
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                for time in discrete_timestamps:
                    # Calculate the weight at time t
                    weight = graph[(i, j)](time)
                    # Add the weight to the DataFrame
                    df.loc[(i, j, time), 'value'] = weight
    return df
