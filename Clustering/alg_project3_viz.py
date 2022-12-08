"""
Creating and visualizing clusters of county-based cancer risk data
using three different clustering algorithms
"""

import math
import urllib.request
from alg_cluster import Cluster
from project_3 import kmeans_clustering, hierarchical_clustering
from alg_clusters_matplotlib import plot_clusters


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib.request.urlopen(data_url)
    data_text = str(data_file.read(), "utf-8")
    data_lines = data_text.split('\n')

    print ("Loaded", len(data_lines), "data points")

    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


def sequential_clustering(singleton_list, num_clusters, *_):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters 
    based on its alphabetical ordering.
    
    This method may return num_clusters or num_clusters + 1 final clusters
    """
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

def run_visualization(url):
    """
    Load a data table, compute a list of clusters and 
    visualize the results
    """
    # get the necessary parameters from user input
    print('\n<<< PARAMETER RETRIEVAL >>>\n')
    while True:
        clustering_type = input("Choose a type of the clustering.\nValid entries: 'kmeans' or 'hierarchical' or 'sequential'\n")
        if clustering_type not in {'kmeans', 'hierarchical', 'sequential'}:
            print(">>> Invalid clustering type.\n")
        else:
            break
    clust_funcs ={'kmeans': kmeans_clustering, 'hierarchical': hierarchical_clustering, \
                  'sequential': sequential_clustering}
    if clustering_type == 'kmeans':
        while True:
            num_iter = int(input("Choose a number of iterations for k-means clustering.\Recommended value: 5\n"))
            if num_iter < 0:
                print(">>> Invalid number of iterations.\n")
            else:
                break    
    else:
        num_iter = None
    while True:
        num_clusters = int(input("Choose a number of clusters.\Accepted values: between 0 and 16\n"))
        if num_clusters < 0 or num_clusters > 16:
            print(">>> Invalid number of clusters.\n")
        else:
            break
    while True:
        cluster_centers = input("Do you want to display cluster centers?\nValid entries: 'yes' or 'no'\n")
        if cluster_centers not in {'yes', 'no'}:
            print(">>> Invalid choice.\n")
        else:
            break   
    center_viz = {'yes': True, 'no': False}

    data_table = load_data_table(url)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    cluster_list = clust_funcs[clustering_type](singleton_list, num_clusters, num_iter)
    print (f"Displaying {len(cluster_list)} {clustering_type} clusters")

    # draw the clusters using matplotlib
    plot_clusters(data_table, cluster_list, center_viz[cluster_centers])

    print("\n<<< Done >>>\n")
    

if __name__ == '__main__':
    # URLs for cancer risk data tables of various sizes
    # Numbers indicate number of counties in data table
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
    DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

    run_visualization(DATA_111_URL)