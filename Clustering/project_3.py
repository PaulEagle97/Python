"""

"""

import math
import alg_cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    min_dist, idx1, idx2 = math.inf, -1, -1

    for cluster_idx1 in cluster_list:
        for cluster_idx2 in cluster_list:
            if cluster_idx1 == cluster_idx2:
                break
            curr_dist = pair_distance(cluster_list, cluster_idx1, cluster_idx2)
            if curr_dist < min_dist:
                min_dist = curr_dist
                idx1 = cluster_idx1
                idx2 = cluster_idx2
    
    return min_dist, idx1, idx2


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    cluster_num = len(cluster_list)
    if cluster_num <= 3:
        return slow_closest_pair(cluster_list)

    mid_idx = cluster_num // 2
    dist_l, idx1_l, idx2_l = fast_closest_pair(cluster_list[ :mid_idx])
    dist_r, idx1_r, idx2_r = fast_closest_pair(cluster_list[mid_idx: ])

    if dist_l < dist_r:
        min_dist = dist_l
        idx1 = idx1_l
        idx2 = idx2_l
    else:
        min_dist = dist_r
        idx1 = idx1_r + mid_idx
        idx2 = idx2_r + mid_idx

    horiz1 = cluster_list[mid_idx - 1].horiz_center()
    horiz2 = cluster_list[mid_idx].horiz_center()
    mid = (horiz1 + horiz2) / 2

    dist_strip, idx1_strip, idx2_strip = closest_pair_strip(cluster_list, mid, min_dist)

    if dist_strip < min_dist:
        min_dist = dist_strip
        idx1 = idx1_strip
        idx2 = idx2_strip

    return min_dist, idx1, idx2


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """

    return ()
            
 
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []

