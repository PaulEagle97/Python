"""
"""
import random
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from alg_cluster import Cluster
from project_3 import slow_closest_pair, fast_closest_pair, hierarchical_clustering, kmeans_clustering
from alg_project3_viz import load_data_table


def gen_random_clusters(num_clusters):
    '''
    Creates a list of clusters 
    where each cluster in this list corresponds 
    to one randomly generated point in the square 
    with corners (±1,±1).
    '''
    return [Cluster(set([]), random.uniform(-1, 1), random.uniform(-1, 1), 0, 0) for _ in range(num_clusters)]


def compute_distortion (cluster_list, data_table):
    '''
    Computes a total distortion for a clustering
    specified as (cluster_list)
    '''
    distortion = 0
    for cluster in cluster_list:
        cluster_error = cluster.cluster_error(data_table)
        distortion += cluster_error

    return distortion


def fast_vs_brute (num_clusters):
    '''
    Computes the running times for (slow_closest_pair)
    and (fast_closest_pair) functions applied to
    a random-generated list with (num_clusters) clusters
    '''
    #create a random list of clusters
    cluster_list = gen_random_clusters(num_clusters)

    #measure the run time for the optimized func
    start = timer()
    _ = fast_closest_pair(cluster_list)
    end = timer()
    fast_time = end - start

    #measure the run time for the brute force func
    start = timer()
    _ = slow_closest_pair(cluster_list)
    end = timer()    
    brute_time = end - start

    return fast_time, brute_time


def plot_efficiency (min_size, max_size):
    """
    Computes and plots the efficiency of (fast_closest_pair)
    and (slow_closest_pair), as a function of running time and
    number of processed clusters. 
    """
    x_vals = []
    y_vals_fast = []
    y_vals_brute = []
    for num_clusters in range (min_size, max_size + 1):
        x_vals.append(num_clusters)
        #compute the run times for both funcs and append to y-values
        run_times = fast_vs_brute(num_clusters)
        y_vals_fast.append(run_times[0])
        y_vals_brute.append(run_times[1])

    #assign title and axis names
    plt.title('(fast_closest_pair) and (slow_closest_pair) efficiency comparison')
    plt.xlabel('Number of clusters')
    plt.ylabel('Running time')  
    
    #plot the run times
    plt.plot(x_vals, y_vals_fast, '-b', label = 'Fast')
    plt.plot(x_vals, y_vals_brute, '-r', label = 'Brute force')
    plt.legend(loc = 'upper left', title = f'({min_size}, {max_size})')

    #exhibit the graphs
    plt.show()


if __name__ == '__main__':

    #plot_efficiency(2, 200)

    NUM_CLUSTERS = 9
    NUM_ITER = 5
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

    data_table = load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    cluster_list = kmeans_clustering(singleton_list, NUM_CLUSTERS, NUM_ITER)
    distortion = compute_distortion(cluster_list, data_table)
    print ('Distortion:', distortion)
    
