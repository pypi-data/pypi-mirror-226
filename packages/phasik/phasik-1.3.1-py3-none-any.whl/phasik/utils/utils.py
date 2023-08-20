"""
Utility functions
"""

import numpy as np


def get_extrema_of_binary_series(binary_series, times):
    """Get data determining intervals during which a binary series is at a minimum (0) or maximum (1)

    For a binary series, let a minimum denote a point at which a 0 changes to a 1, and let a maximum denote a point at
    which a 1 changes to a 0.

    Parameters
    ----------
    binary_series : ndarray of bool
        Binary array (0s and 1s only) representing a series of binary data
    times : list_like
        ndarray of time points corresponding to the series above

    Returns
    -------
    mins : ndarray
        1D array of time points [a_1, a_2, ..., a_n] such that for all i the series has value 1 at time a_i and
        does NOT have value 1 at time a_i - 1 (either because it has value 0 or because there is no point a_i - 1)
    maxs : ndarray
        1D array of time points [b_1, b_2, ..., b_n] such that for all i the series has value 1 at time b_i and
        does NOT have value 1 at time b_i + 1 (either because it has value 0 or because there is no point b_i + 1)
    """

    binary = 1 * binary_series
    slopes = np.diff(binary)

    mins = []
    maxs = []

    if binary[0] == 1:
        mins.append(times[0])

    if binary[-1] == 1:
        maxs.append(times[-1])

    for i in range(len(slopes)):
        if slopes[i] == 1:
            mins.append(times[i + 1])
        elif slopes[i] == -1:
            maxs.append(times[i])

    return mins, maxs
