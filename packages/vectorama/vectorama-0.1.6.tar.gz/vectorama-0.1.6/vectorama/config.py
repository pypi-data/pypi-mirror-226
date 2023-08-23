from pydantic import ConfigDict


class VectoramaConfig(ConfigDict, total=False):
    """
    Desired total number of clusters. This is used as an absolute figure; we will
    always initialize at least |desired_cluster_count| clusters.

    """

    desired_cluster_count: int

    """
    The desired size of each cluster. This is used in expectation, so we attempt
    to balance clusters out to roughly size |desired_cluster_size|.

    """
    desired_cluster_size: int

    """
    The amount of records that are stored in one text-file. This is expected to be able to quickly
    load the data into memory. If your record sizes are large, you likely want to decrease this value.
    Defaults to 1000.
 
    """
    chunk_size: int

    """
    The threshold for the skew of the cluster sizes. This is defined as the relative difference between the
    euclidean norms of the fixed centroid and the new datapoint average. If the skew is larger than this
    value, we will reindex the cluster. Defaults to 0.1.

    """
    require_reindex_skew_threshold: float

    """
    The threshold for the change in the size of the change log. If each cluster has more than this quantity of objects
    inserted, we will perform a reindex. Defaults to 1000.

    """
    require_reindex_change_log_size: int
