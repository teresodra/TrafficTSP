import pandas as pd


def discretise_and_approximate_graph(graph: dict, bins: int) -> dict:
    """
    Discretises the weight of the graph from a continuous function
    to a finite set.
    Also, these weights are approximated to the closer timestamp.
    """
    n_nodes = graph['n_nodes']
    time_range = graph['time_range']
    if bins <= 1:
        timestep = time_range[1] - time_range[0]
    else:
        timestep = (time_range[1] - time_range[0])/(bins - 1)

    rows = []
    # Iterate over all the edges
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                for step in range(bins):
                    # Calculate the weight at time t
                    weight_funct = graph[(i, j)]
                    t = step * timestep
                    weight = weight_funct(t)
                    # Add the weight to the DataFrame
                    new_row = {'start_node': i,
                               'final_node': j,
                               'time': step,
                               'travel_time': round(weight/timestep)}
                    rows.append(new_row)

    # Create DataFrame from rows
    df = pd.DataFrame(rows,
                      columns=['start_node', 'final_node',
                               'time', 'travel_time'])
    return df
