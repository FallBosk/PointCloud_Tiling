# PointCloudTiling, GPL-3.0 license

""" 
Mathematical utility methods - Module (Python)

The module is adapted from:
https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Processing
"""

import numpy as np
from numba import jit


@jit(nopython=True, cache=True, parallel=True)
def get_octree_level(points, grid_size):
    """Compute nearest octree level based on a desired grid_size."""
    dims = np.zeros((points.shape[1],))
    for d in range(points.shape[1]):
        dims[d] = np.max(points[:, d]) - np.min(points[:, d])
    max_dim = np.max(dims)
    if max_dim < 0.001:
        return 0
    octree_level = np.rint(-np.log(grid_size / max_dim) / (np.log(2)))
    if octree_level > 0:
        return np.int64(octree_level)
    return 1