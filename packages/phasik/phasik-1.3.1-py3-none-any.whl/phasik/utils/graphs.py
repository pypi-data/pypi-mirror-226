"""
Utility functions for static graphs
"""

import networkx as nx
import numpy as np
import pandas as pd

__all__ = [
    "graph_size_info",
    "weighted_edges_as_df",
]


def graph_size_info(graph):
    """Return basic size info on about graph"""
    return f"{len(graph)} nodes and {len(graph.edges)} edges"


def weighted_edges_as_df(network, keep_static=True, temporal_edges=None):
    """Returns a pandas.Dataframe of weighted edges sorted by weight,
    from a networkx.Graph.

    Columns are ['i', 'j', 'weight'] and each row represents a different edge

    Parameters
    ----------
    network : networkx.Graph
        A network from which to get weighted edges
    keep_static : bool or np.nan, optional
        If True (default), keep all edges. If False,
        discard the static edges (those not in `temporal_edges`).
        If np.nan, keep the static edges, but set their weight to np.nan.
        If keep_static is not False, `temporal_edges` must be provided.
    temporal_edges : list of tuples
        List of edges for which there is temporal information.

    Returns
    -------
    pandas.DataFrame

    Notes
    -----
    When the static network is derived from a temporal network,
    some edges might static (no temporal info) and have a default
    constant edge weight. That is when the arguments `keep_static`
    and `temporal_edges` are useful.

    """

    if not keep_static and temporal_edges is None:
        raise ValueError(
            "If keep_static is True, temporal_edges must be a list of edges"
        )

    edges_weighted = [(i, j, network[i][j]["weight"]) for (i, j) in network.edges]

    if not keep_static:  # discard edges without temporal info
        edges_weighted = [
            (i, j, w) for (i, j, w) in edges_weighted if (i, j) in temporal_edges
        ]

    elif np.isnan(keep_static):  # set nan weigth for edges without temporal info

        edges_temporal = [
            (i, j, w) for (i, j, w) in edges_weighted if (i, j) in temporal_edges
        ]

        edges_nan = [
            (i, j, np.nan)
            for (i, j, w) in edges_weighted
            if (i, j) not in temporal_edges
        ]

        edges_weighted = edges_temporal + edges_nan

    edges_weighted_df = pd.DataFrame(edges_weighted, columns=["i", "j", "weight"])
    edges_weighted_df = edges_weighted_df.sort_values(
        by="weight", ascending=False, na_position="last"
    )

    return edges_weighted_df
