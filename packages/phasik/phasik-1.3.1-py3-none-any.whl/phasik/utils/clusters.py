"""
Functions to manipulate and sort clusters
"""

from copy import deepcopy

import numpy as np
from sklearn.metrics import adjusted_rand_score

__all__ = [
    "aggregate_network_by_cluster",
    "convert_cluster_labels_to_dict",
    "rand_index_over_methods_and_sizes",
    "cluster_sort",
]


def aggregate_network_by_cluster(
    temporal_network, clusters, sort_clusters=None, output="averaged"
):
    """Aggregates the temporal network over eacher cluster in a cluster set


    Parameters
    ----------
    temporal_network : phasik.TemporalNetwork
        Temporal network to aggregate
    clusters : array of int
        Cluster labels
    sort_clusters : bool
        If True, sort cluster labels based on ascending times
    output : {'weighted', 'averaged', 'binary', 'normalised'}, optional
            Determines the type of output edge weights

    Returns
    -------
    aggregates : dict
        Dict each key is a cluster label and each value is a tuple
        of the form (networkx.Graph, list of time indices of cluster).
    """

    aggregates = {}

    if sort_clusters is True:  # sort by ascending times
        clusters = cluster_sort(clusters)
    elif (sort_clusters is False) or (sort_clusters is None):
        pass
    elif isinstance(sort_clusters, list):  # sort by specified order
        clusters = cluster_sort(clusters, final_labels=sort_clusters)
    else:
        raise ValueError(
            "Invalid value for 'sort_clusters': must be True or a list of cluster labels"
        )

    cluster_time_indices = convert_cluster_labels_to_dict(clusters)

    for cluster_label, time_indices in cluster_time_indices.items():

        aggregates[cluster_label] = (
            temporal_network.aggregated_network(
                time_indices=time_indices, output=output
            ),
            time_indices,
        )

    return aggregates


def convert_cluster_labels_to_dict(clusters):
    """Returns dictionary where each key is a cluster label and each
    value is list of the time indices composing the cluster

    Parameters
    ----------
    clusters : list of int
        List of cluster labels

    Return
    ------

    """
    n_max = max(clusters)

    cluster_times = {n: list(np.where(clusters == n)[0]) for n in range(1, n_max + 1)}

    return cluster_times


def rand_index_over_methods_and_sizes(valid_cluster_sets, reference_method="ward"):
    """
    Compute the Rand Index to compare any clustering method to a reference method, for all combinations of methods
    and number of clusters.

    Parameters
    ----------
    valid_cluster_sets : list
        List of tuples (cluster_object, method_name) representing the clustering object and the name of the
        clustering method used to obtain it.
    reference_method : str, optional
        The name of the reference method to compare against. The default is "ward".

    Returns
    -------
    rand_scores : ndarray
        Array of dimension (n_sizes, n_methods) with Rand Index scores.

    Notes
    -----
    The Rand Index is a measure of the similarity between two clusterings. It is based on the number of pairs of
    samples that are assigned to the same or different clusters in the two clusterings. The adjusted Rand Index is a
    modification of the Rand Index that takes into account chance agreements.
    """

    # Extract the list of methods used to obtain the clusters and the reference method
    valid_methods = [sets[1] for sets in valid_cluster_sets]

    # Find the index of the reference method
    i_ref = valid_methods.index(reference_method)

    # Extract the clusters obtained with the reference method
    clusters_ref = valid_cluster_sets[i_ref][0]

    # Compute Rand Index to compare each method with reference method, for each number of clusters
    n_sizes = len(clusters_ref.n_clusters)
    n_methods = len(valid_cluster_sets)
    rand_scores = np.zeros((n_sizes, n_methods))

    for i_size, size in enumerate(clusters_ref.n_clusters):
        for i_method, method in enumerate(valid_methods):

            # Extract the clusters obtained with the current method
            clusters2 = valid_cluster_sets[i_method][0]

            # Compute the Rand Index between the two clusterings
            rand_index = adjusted_rand_score(
                clusters_ref.clusters[i_size], clusters2.clusters[i_size]
            )

            # Store the Rand Index in the results array
            rand_scores[i_size, i_method] = rand_index

    return rand_scores


def cluster_sort(clusters, final_labels=None):
    """
    Sorts an array of cluster labels in order of appearance, and returns the sorted array while leaving the original clusters unchanged.

    Parameters
    ----------
    clusters : numpy.ndarray
        An array of cluster labels.
    final_labels : list or None, optional
        A list of final labels (as integers) to replace the original cluster labels, by default None.

    Returns
    -------
    numpy.ndarray or list
        An array of cluster labels sorted in order of appearance. If `final_labels` is not None, it will return a list of final labels with the same length as `clusters`.

    Examples
    --------
    >>> clusters = np.array([2, 2, 2, 3, 3, 1, 1, 1])
    >>> cluster_sort(clusters)
    array([1, 1, 1, 2, 2, 3, 3, 3])

    >>> final_labels = [4, 5, 6]
    >>> cluster_sort(clusters, final_labels)
    [4, 4, 4, 5, 5, 6, 6, 6]

    """

    # give temporary negative values to labels
    arr = -clusters

    i = 1
    for j, el in enumerate(arr):
        if el >= 0:  # already sorted
            pass
        else:  # give new label
            arr[arr == el] = i
            i += 1

    # if final_labels is a list, replace each element of the array with the corresponding label
    if isinstance(final_labels, list):
        arr = list(map(lambda i: final_labels[i - 1], arr))

    # check that the clustering has not changed
    assert adjusted_rand_score(clusters, arr) == 1

    return arr
