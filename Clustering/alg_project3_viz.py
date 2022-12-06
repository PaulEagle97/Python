"""
Example code for creating and visualizing
cluster of county-based cancer risk data
"""

import math
import random
import urllib.request
import alg_cluster
import project_3
import alg_clusters_matplotlib


###################################################
# Code to load data tables

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


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
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
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results

def run_visualization(url):
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters
    """
    data_table = load_data_table(url)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    #cluster_list = sequential_clustering(singleton_list, 15)	
    #print ("Displaying", len(cluster_list), "sequential clusters")

    #cluster_list = project_3.hierarchical_clustering(singleton_list, 9)
    #print ("Displaying", len(cluster_list), "hierarchical clusters")

    cluster_list = project_3.kmeans_clustering(singleton_list, 9, 5)	
    print ("Displaying", len(cluster_list), "k-means clusters")

    # draw the clusters using matplotlib
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
    #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    

if __name__ == '__main__':
    # URLs for cancer risk data tables of various sizes
    # Numbers indicate number of counties in data table
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
    DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

    run_visualization(DATA_896_URL)