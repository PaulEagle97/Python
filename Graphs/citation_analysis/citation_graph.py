"""
Application #1 of the course "Algorithmic Thinking (Part 1)"

This is a set of functions for analyzing the in-degree distribution of graphs, which are represented using dictionaries.
If run as a script, it loads and analyses a provided citation graph for 27,770 high-energy physics theory papers.
"""
import os
import sys
import math
import matplotlib.pyplot as plt
import urllib.request

#importing plotting function from another module
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, os.pardir))
from plot_graph import plot


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib.request.urlopen(graph_url)
    graph_text = str(graph_file.read(), "utf-8")
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print (">>> Loaded graph with", len(graph_lines), "nodes.")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def graph_val_gen(graph):
    """
    A generator for the neighbors for each graph node
    """
    for value in graph.values():
        yield value


def bin_search(a_list, val, low, high):
    """
    Performs an iterative binary search in (a_list)
    """
    while low <= high:                
        mid = (low + high) // 2
        if val == a_list[mid]:
            return mid
        elif val > a_list[mid]:
            low = mid + 1
        else:
            high = mid - 1    
    
    return - 1
 

def left_right_count(target_pos, neigh_list, node):
    """
    Counts the total number of occurrences of a node in a sorted neigh_list
    after receiving the index of the first occurrence found by the binary search
    """
    counter = 0
    if target_pos >= 0:
        counter += 1
        #count the number of occurrences to the left of the guessed value
        target_pos_left = target_pos - 1
        valid_ind = (target_pos_left >= 0)            
        while valid_ind and neigh_list[target_pos_left] == node:
            counter += 1
            target_pos_left -= 1
            if target_pos_left < 0:
                valid_ind = False
        #count the number of occurrences to the right of the guessed value            
        target_pos_right = target_pos + 1
        valid_ind = (target_pos_right <= len(neigh_list) - 1)
        while valid_ind and neigh_list[target_pos_right] == node:
            counter += 1
            target_pos_right += 1
            if target_pos_right == len(neigh_list):
                valid_ind = False
        #adjust the lower boundary for the next binary search
        low = target_pos    
    
    return counter
    
    
def compute_in_degrees(digraph):
    """
    Returns a dictionary with keys corresponding to nodes in digraph 
    and in-degrees for each node as values
    (node_num ---> node_in_degree)
    """
    in_degrees = {}
    neigh_list = []
    val_gen_func = graph_val_gen(digraph)
    #create a sorted list with all neighbor values of the graph
    for neighbors in val_gen_func:
        neigh_list.extend(list(neighbors))
    neigh_list.sort()
    #create a sorted list with all nodes of the graph
    nodes_list = list(digraph.keys())
    nodes_list.sort()
    #initialize boundary for binary search
    low = 0
    high = len(neigh_list) - 1
    #iterate over each node of the graph and calculate its in_degree
    for node in nodes_list:
        #localize a position of the node occurrence/s in the neighbor list
        #return -1 if it is not found
        first_guess_pos = (bin_search(neigh_list, node, low, high))
        #compute the number of its occurrences in the neighbor list
        #and assign this value to the respective node/key
        in_degrees[node] = left_right_count(first_guess_pos, neigh_list, node)
    
    return in_degrees     


def compute_out_degrees(digraph):
    '''
    Returns a dictionary with keys corresponding to nodes in digraph 
    and out-degrees for each node as values
    (node_num ---> node_out_degree)
    '''
    out_degrees = {}
    for node in digraph:
        out_degrees[node] = len(digraph[node])
    
    return out_degrees


def in_degree_distribution(digraph):
    """
    Returns a dictionary with keys corresponding to in-degrees in the graph 
    and normalized number of their occurrences as values
    (in_degree ---> num_occurrencies)
    """
    #initialize and compute the dictionary {nodes ---> in-degrees}
    deg_dist = {}
    in_degrees = compute_in_degrees(digraph)
    #compute the list of all degree occurrences
    degrees_list = list(in_degrees.values())
    #for each degree, count how many times it occurres in the list
    for degree in set(degrees_list):
        deg_dist[degree] = degrees_list.count(degree) / len(degrees_list)
    
    return deg_dist


def convert_to_log(a_dict):
    """
    Converts all keys(except 0) and all values in a dictionary a_dict to a log scale
    """
    log_dict = {}
    for key in a_dict.keys():
        if key != 0:
            log_key = math.log(key)
            log_val = math.log(a_dict[key])
            log_dict[log_key] = log_val
        
    return log_dict
    

def main():
    """
    Loads a real citation graph, computes and plots its in-degree distribution.
    """
    #get the plot type from the user
    print('\n<<< PARAMETER RETRIEVAL >>>\n')
    while True:
        plot_type = input("Choose a type of the plot.\nValid entries: 'normal' or 'log'\n")
        if plot_type not in {'normal', 'log'}:
            print(">>> Invalid plot type.\n")
        else:
            break

    #load the citation graph
    CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
    citation_graph = load_graph(CITATION_URL)
    GRAPH_TYPE = 'Citation'

    #compute distributions
    citation_dist_norm = in_degree_distribution(citation_graph)
    citation_dist_norm_log = convert_to_log(citation_dist_norm)

    # plot the distribution
    plot(citation_dist_norm, citation_dist_norm_log, plot_type, GRAPH_TYPE)

    print('\n<<< Done >>>\n')


if __name__ == '__main__':
    main()

