import pandas as pd
import numpy as np


def discretise_and_approximate_graph(graph: dict, bins: int) -> dict:
    """
    Discretises the weight of the graph from a continuous function
    to a finite set.
    Also, these weights are approximated to the closer timestamp.
    """
    n_nodes = graph['n_nodes']
    time_range = graph['time_range']
    timestep = (time_range[1] - time_range[0])/(bins - 1)

    # Create the MultiIndex for the DataFrame
    multi_index = pd.MultiIndex.from_product(
        [range(n_nodes), range(n_nodes), range(bins)],
        names=['start_node', 'final_node', 'time']
    )

    # Initialize the DataFrame
    df = pd.DataFrame(index=multi_index, columns=['cost'])
    # Iterate over all the edges
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                for step in range(bins):
                    # Calculate the weight at time t
                    t = step * timestep
                    weight = graph[(i, j)](t)
                    # Add the weight to the DataFrame
                    df.loc[(i, j, step), 'value'] = round(weight/timestep)
    return df
