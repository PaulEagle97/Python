"""
Functions for generating random ER graphs
"""
import random
import itertools


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
    from application_1 import in_degree_distribution, convert_to_log
    import matplotlib.pyplot as plt

    NUM_NODES = 5000
    PROBABILITY = 0.3
    PLOT_TYPE = 'NORM'
    GRAPH_TYPE = 'Undirected'

    if GRAPH_TYPE == 'Undirected':
        a_graph = er_ugraph(NUM_NODES, PROBABILITY)
    elif GRAPH_TYPE == 'Directed':
        a_graph = er_digraph(NUM_NODES, PROBABILITY)

    # compute in-degree distribution 
    # and duplicate it on a log/log scale
    in_dist_norm = in_degree_distribution(a_graph)
    in_dist_norm_log = convert_to_log(in_dist_norm)

    # sorted by key, return a list of tuples
    if PLOT_TYPE == 'LOG':
        lists = sorted(in_dist_norm_log.items())
    else:
        lists = sorted(in_dist_norm.items())

    # unpack a list of pairs into two tuples
    x, y = zip(*lists) 

    plt.plot(x, y)

    if PLOT_TYPE == 'LOG':
        plt.xlabel('log(Number of in-degrees)')
        plt.ylabel('log(Normalized number of occurrences)')
    else:
        plt.xlabel('Number of in-degrees')
        plt.ylabel('Normalized number of occurrences')        
    
    plt.title(f'{GRAPH_TYPE} ER graph in-degree distribution')
    
    plt.show()

    print('<<< Done >>>')


if __name__ == "__main__":
    test()

