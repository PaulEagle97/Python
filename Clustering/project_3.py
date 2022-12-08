"""
This module contains functions for clustering a set of points
with each point representing a specific county in USA with parameters
specified as class instance attributes in (alg_cluster) module
"""

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
    min_dist, idx1, idx2 = float('inf'), -1, -1
    cluster_idxs = range(len(cluster_list))

    for cluster_idx1 in cluster_idxs:
        for cluster_idx2 in cluster_idxs:
            if cluster_idx1 == cluster_idx2:
                break
            curr_dist = pair_distance(cluster_list, cluster_idx1, cluster_idx2)
            if curr_dist[0] < min_dist:
                min_dist = curr_dist[0]
                idx1 = min(cluster_idx1, cluster_idx2)
                idx2 = max(cluster_idx1, cluster_idx2)
    
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
    dist_l, idx_l1, idx_l2 = fast_closest_pair(cluster_list[ :mid_idx])
    dist_r, idx_r1, idx_r2 = fast_closest_pair(cluster_list[mid_idx: ])

    if dist_l < dist_r:
        min_dist = dist_l
        idx1 = idx_l1
        idx2 = idx_l2
    else:
        min_dist = dist_r
        idx1 = idx_r1 + mid_idx
        idx2 = idx_r2 + mid_idx

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
    strip_idxs = []
    min_dist, min_idx1, min_idx2 = float('inf'), -1, -1

    for idx, cluster in enumerate(cluster_list):
        if abs(cluster.horiz_center() - horiz_center) < half_width:
            strip_idxs.append(idx)

    strip_idxs.sort(key = lambda cluster_idx: cluster_list[cluster_idx].vert_center())
    strip_len = len(strip_idxs)

    for idx1 in range(strip_len - 1):
        for idx2 in range(idx1 + 1, min(idx1 + 3, strip_len - 1) + 1):
            curr_dist = pair_distance(cluster_list, strip_idxs[idx1], strip_idxs[idx2])
            if curr_dist[0] < min_dist:
                min_dist = curr_dist[0]
                min_idx1 = min(strip_idxs[idx1], strip_idxs[idx2])
                min_idx2 = max(strip_idxs[idx1], strip_idxs[idx2])

    return min_dist, min_idx1, min_idx2
            

def hierarchical_clustering(cluster_list, num_clusters, *_):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        _, idx1, idx2 = fast_closest_pair(cluster_list)

        cluster1, cluster2 = cluster_list[idx1], cluster_list[idx2]
        cluster1.merge_clusters(cluster2)
        cluster_list.remove(cluster2)

    return cluster_list


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    old_clusters = sorted(cluster_list, key = lambda cluster: cluster.total_population(), reverse=True)[ :num_clusters]
    for _ in range (num_iterations):
        new_clusters = []
        for _ in range (num_clusters):
            new_clusters.append(alg_cluster.Cluster(set([]), 0, 0, 0, 0))
        for county in cluster_list:
            min_dist = float('inf')
            for idx, cluster in enumerate(old_clusters):
                curr_dist = county.distance(cluster)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    closest_cluster_idx = idx
            new_clusters[closest_cluster_idx].merge_clusters(county)
        old_clusters = list(new_clusters)

    return old_clusters

