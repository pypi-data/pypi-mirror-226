"""
Functions to convert input data from one format to another
"""

from itertools import combinations

import pandas as pd

__all__ = ["convert_edge_timeseries_to_tedges", "convert_node_to_edge_timeseries"]


def convert_edge_timeseries_to_tedges(edge_timeseries):
    """Converts edge timeseries to DataFrame of tedges

    Note: since all timeseries have the same number of timepoints, many rows in the tedges might have a zero weight

    Parameters
    ----------
    edge_timeseries : pandas.DataFrame
        Time series indexed by edge name and where columns are timepoints

    Returns
    -------
    tedges : pandas.DataFrame

    """
    # series_df = pd.DataFrame.from_dict(edge_timeseries, orient="index", columns=times)
    series_stack = edge_timeseries.stack()  # times are second index now
    series_stack = series_stack.to_frame("weight")
    tedges = series_stack.reset_index()  # set multindex (edge, time) as columns
    tedges[["i", "j"]] = tedges["level_0"].str.split(
        "-", expand=True
    )  # split edge as columns 'i' and 'j'
    del tedges["level_0"]
    tedges.columns = ["t", "weight", "i", "j"]  # rename
    tedges = tedges[["i", "j", "t", "weight"]]  # reorder

    return tedges


def convert_node_to_edge_timeseries(
    node_series, combine=lambda x, y: x * y, static_edges=None
):
    """Convert node timeseries to edge timeseries

    Parameters
    ----------
    node_series : pandas.DataFrame
        Node timeseries, indexed by node names and where columns are times
    combine : function
        Function to use to combine two node time series into one edge time series
    static_edges : list of tuples
        List of edges in static network. If None (default), considers fully connected network between nodes

    Returns
    -------
    edge_series : pd.DataFrame
        Dataframe containing edge timeseries, indexed by edge name 'A-B', columns are times, and entries are weights
    """

    edge_series_dict = {}

    #     node_series = node_series.sort_index() # to ensure that intersection later contains all edges

    if static_edges is None:
        static_edges = combinations(node_series.index, 2)

    all_potential_edges = combinations(node_series.index, 2)

    #     edges = set(static_edges).intersection(all_potential_edges)

    # ordering of nodes inside each edge is not guaranteed to be the same in those lists
    # so to ensure the right intersection, we need to sort or use frozensets
    set1 = {frozenset(edge) for edge in static_edges}
    set2 = {frozenset(edge) for edge in all_potential_edges}
    set3 = set1.intersection(set2)

    edges = [
        tuple(edge) for edge in set3
    ]  # list of edges in static network with temporal information

    for edge in edges:
        edge_name = "-".join(edge)
        u, v = edge
        series = combine(node_series.loc[u], node_series.loc[v])
        edge_series_dict[edge_name] = series

    edge_series = pd.DataFrame.from_dict(edge_series_dict, orient="index")

    return edge_series
