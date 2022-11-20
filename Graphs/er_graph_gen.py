"""
Functions for generating random ER graphs
"""
import os
import sys
import random
import itertools
from plot_graph import plot

#importing necessary functions from another module
sys.path.append(os.path.dirname(__file__) + '\citation_analysis')
from citation_graph import in_degree_distribution, convert_to_log


def er_digraph(num_nodes, prob):
    """
    A generator of directed graphs with adjustable probability of edge creation
    """
    #compute all the node indices
    all_nodes = set(range(num_nodes))

    #compute all of the node permutations of size 2 (directed edges)
    all_edges = itertools.permutations(all_nodes, 2)

    valid_edges = set()
    #assign every edge from all_edges to valid_edges with prob probability
    for edge in all_edges:
        rand_val = random.random()
        if rand_val < prob:
            valid_edges.add(edge)

    #create an output dictionary
    a_graph = {}

    #for each valid edge, check whether its 'tail' 
    #already exists as a node/key in the dictionary 
    for edge in valid_edges:
        #if yes, then add its 'head' to the set of values of the node
        if edge[0] in a_graph:
            a_graph[edge[0]].update([edge[1]])
        #if not, create a new node with the key equal to its 'tail'
        #and the value from its 'head'
        else:
            a_graph[edge[0]] = set([edge[1]])
            
    #check for nodes with no values 
    #and add them with an empty set() value
    empty_nodes = all_nodes.difference(set(a_graph))
    for node in empty_nodes:
        a_graph.setdefault(node, set())        
    
    return a_graph


def er_ugraph(num_nodes, prob):
    """
    A generator of undirected graphs with adjustable probability of edge creation
    """
    #compute all the node indices
    all_nodes = set(range(num_nodes))

    #compute all of the node combinations of size 2 (undirected edges)
    all_edges = itertools.combinations(all_nodes, 2)

    #create an output dictionary
    a_graph = {}

    #start iterating over all edges
    for edge in all_edges:
        #choose random edges with (prob) probability
        rand_val = random.random()
        if rand_val < prob:
            #iterate over both nodes in each edge        
            for node in edge:
                #evaluate the second node in each pair as a set
                second_node = set(edge).difference({node})
                if node in a_graph:
                    #add second node to the (node) neighbors
                    a_graph[node].update(second_node)
                else:
                    #create new node in the (a_graph)
                    a_graph[node] = second_node

    #check for nodes with no values 
    #and add them with an empty set() value
    empty_nodes = all_nodes.difference(set(a_graph))
    for node in empty_nodes:
        a_graph.setdefault(node, set())        
    
    return a_graph


def test():
    '''
    Creates a sample graph of a certain type, with adjustable parameters,
    and then plots it on a normal or log/log scale.    
    '''
    # get the necessary parameters from user input
    print('\n<<< PARAMETER RETRIEVAL >>>\n')
    while True:
        num_nodes = int(input("Choose a number of nodes for the ER graph.\nRecommended value: < 5000\n"))
        if num_nodes < 0:
            print(">>> The number of nodes cannot be negative.\n")
        else:
            break
    while True:
        probability = float(input("Choose a probability of edge creation.\n"))
        if not 0 <= probability <= 1:
            print(">>> The probability must be between 0 and 1.\n")
        else:
            break
    while True:
        graph_type = input("Choose a type of the graph.\nValid entries: 'undirected' or 'directed'\n")
        if graph_type not in {'undirected', 'directed'}:
            print(">>> Invalid graph type.\n")
        else:
            break
    while True:
        plot_type = input("Choose a type of the plot.\nValid entries: 'normal' or 'log'\n")
        if plot_type not in {'normal', 'log'}:
            print(">>> Invalid plot type.\n")
        else:
            break
    
    # create a random graph with the provided parameters
    if graph_type == 'undirected':
        a_graph = er_ugraph(num_nodes, probability)
    else:
        a_graph = er_digraph(num_nodes, probability)

    # compute in-degree distribution 
    # and duplicate it on a log/log scale
    in_dist_norm = in_degree_distribution(a_graph)
    in_dist_norm_log = convert_to_log(in_dist_norm)

    # plot the distribution
    plot(in_dist_norm, in_dist_norm_log, plot_type, graph_type)

    print('\n<<< Done >>>\n')


if __name__ == "__main__":
    test()

