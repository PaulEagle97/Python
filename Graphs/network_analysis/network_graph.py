'''
Application #2 of the course "Algorithmic Thinking (Part 1)"

This is a set of functions for analyzing the connectivity of a computer network as it undergoes a cyber-attack,
as well as an efficiency between a brute force and optimized algorithms for computing the attack order.

If run as a script, it can follow one of two routes:
1) Loads and analyses a real network graph and compares its resilience to two generic types of random graphs.
2) Runs two functions with an input, determined by a user, and analyses their run times.
'''
import os
import sys
import random
from copy import deepcopy
import matplotlib.pyplot as plt
from timeit import default_timer as timer

#importing necessary functions from other modules
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, os.pardir))
sys.path.append(os.path.join(path, os.pardir) + '\citation_analysis')
from graph_resilience import compute_resilience
from dpa_upa_graph_gen import dpa_upa_graph
from er_graph_gen import er_ugraph
from citation_graph import load_graph


def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph (ugraph)
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def fast_targeted_order(ugraph):
    '''
    A more efficient version of (targeted_order)
    Compute a targeted attack order consisting
    of nodes of maximal degree.
    
    Returns:
    A list of nodes
    '''
    # Creates a list (degree_sets) whose k-th element 
    # is the set of nodes of degree k
    new_graph = deepcopy(ugraph)
    degree_sets = [set([]) for _ in range(len(new_graph))]
    for node in new_graph:
        degree = len(new_graph[node])
        degree_sets[degree].update({node})

    attack_order = []
    # Iterates through the list (degree_sets) in order of decreasing degree.
    for a_degree in range(len(new_graph)-1, -1, -1):
        # When it encounters a non-empty set, 
        # the nodes in this set must be of maximum degree.
        while degree_sets[a_degree] != set([]):
            # Then it repeatedly chooses a node from this set, 
            a_node = random.choice(list(degree_sets[a_degree]))
            # deletes that node from the graph, and updates (degree_sets).
            degree_sets[a_degree].difference_update({a_node})            
            for neighbor in new_graph[a_node]:
                neigh_degree = len(new_graph[neighbor])
                degree_sets[neigh_degree].difference_update({neighbor})
                degree_sets[neigh_degree-1].update({neighbor})
            
            attack_order.append(a_node)
            delete_node(new_graph, a_node)

    return attack_order


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree.
    Brute force algorithm.

    Returns:
    A list of nodes
    """
    #copy the graph and initialize the attack order list
    new_graph = deepcopy(ugraph)
    order = [] 
    #run until there are no nodes left in the graph   
    while len(new_graph) > 0:
        max_degree = -1
        #compute a node of the maximum degree in the graph
        for node in new_graph:
            node_neigh = new_graph[node]
            if len(node_neigh) > max_degree:
                max_degree = len(node_neigh)
                max_degree_node = node
        #delete this node from the graph
        delete_node (new_graph, max_degree_node)
        #add the node to the attack order
        order.append(max_degree_node)
    
    return order
    

def random_order(a_graph):
    '''
    Receives graph and returns a randomly shuffled list of its nodes.
    '''
    graph_nodes = list(a_graph.keys())
    random.shuffle(graph_nodes)

    return graph_nodes


def compute_num_edges (a_graph, is_undirected = True):
    '''
    Computes the number of edges in (a_graph)
    '''
    num_edges = 0

    for neighbors in a_graph.values():
        num_edges += len(neighbors)
    
    if is_undirected:
        num_edges /= 2

    return int(num_edges)    


def fast_vs_brute(num_nodes, m_param):
    '''
    Computes the running times for (targeted_order)
    and (fast_targeted_order) functions applied to
    a random-generated UPA graph with (num_nodes) and (m_param)
    '''
    #create a random UPA graph
    a_graph = dpa_upa_graph (num_nodes, m_param, 'UPA')

    #measure the run time for the optimized func
    start = timer()
    _ = fast_targeted_order(a_graph)
    end = timer()
    fast_time = end - start

    #measure the run time for the brute force func
    start = timer()
    _ = targeted_order(a_graph)
    end = timer()    
    brute_time = end - start

    return fast_time, brute_time


def plot_resilience(netw_graph, er_graph, upa_graph, attack_type, er_prob, upa_m_param, percentage_removed_nodes = 100):
    '''
    Computes and plots the resilience of 3 graphs 
    depending on the (attack_type) used
    '''
    #define attack order functions
    attack_funcs = {'random' : random_order, 'targeted' : fast_targeted_order}
    
    #compute resiliences for 3 graphs
    netw_resilience = compute_resilience(netw_graph, attack_funcs[attack_type](netw_graph))
    er_resilience = compute_resilience(er_graph, attack_funcs[attack_type](er_graph))
    upa_resilience = compute_resilience(upa_graph, attack_funcs[attack_type](upa_graph))

    #create y-axis lists for the given range defined by (percentage_removed_nodes)
    num_removed_nodes = int(len(netw_resilience) * percentage_removed_nodes / 100)
    x_vals = range(num_removed_nodes)
    y_vals_1 = []
    y_vals_2 = []
    y_vals_3 = []
    for x in x_vals:
        y_vals_1.append(netw_resilience[x])
        y_vals_2.append(er_resilience[x])
        y_vals_3.append(upa_resilience[x])

    #assign title and axis names
    plt.title(f'Comparing resilience between graphs\n({attack_type} attack)')
    plt.xlabel(f'Number of nodes removed (up to {percentage_removed_nodes}%)')
    plt.ylabel('Size of the largest connected component')  
    
    #plot the three resiliences
    plt.plot(x_vals, y_vals_1, '-b', label = 'Computer network')
    plt.plot(x_vals, y_vals_2, '-r', label = f'ER (prob. = {er_prob})')
    plt.plot(x_vals, y_vals_3, '-g', label = f'UPA (m_param = {upa_m_param})')
    plt.legend(loc='upper right')

    #exhibit the graphs
    plt.show()


def plot_efficiency(min_num_nodes, max_num_nodes, step, m_param = 5):
    '''
    Computes and plots the efficiency of (fast_targeted_order)
    and (targeted_order), as a function of running time and the
    size of a processed graph.
    '''
    #create y-axis lists for each number of nodes
    #in the provided interval with a provided (step)
    x_vals = []
    y_vals_fast = []
    y_vals_brute = []
    for num_nodes in range(min_num_nodes, max_num_nodes, step):
        x_vals.append(num_nodes)
        #compute the run times for both funcs and append to y-values
        run_times = fast_vs_brute(num_nodes, m_param)
        y_vals_fast.append(run_times[0])
        y_vals_brute.append(run_times[1])
    
    #assign title and axis names
    plt.title('(fast_targeted_order) and (targeted_order) efficiency comparison')
    plt.xlabel('Number of nodes')
    plt.ylabel('Running time')  
    
    #plot the run times
    plt.plot(x_vals, y_vals_fast, '-b', label = 'Fast')
    plt.plot(x_vals, y_vals_brute, '-r', label = 'Brute force')
    plt.legend(loc = 'upper left', title = f'({min_num_nodes}, {max_num_nodes}, {step})\nm_param = {m_param}')

    #exhibit the graphs
    plt.show()


def resilience():
    '''
    Compares the resiliences between 3 graphs, 
    two of which are created randomly and one
    is provided through an external link.
    '''
    # get the necessary parameters from user input
    print('\n<<< PARAMETER RETRIEVAL >>>\n')
    while True:
        attack_type = input("Choose a type of the attack.\nValid entries: 'random' or 'targeted'\n")
        if attack_type not in {'random', 'targeted'}:
            print(">>> Invalid attack type.\n")
        else:
            break
    while True:
        percentage_removed_nodes = int(input("Choose a percentage of nodes to be removed.\n"))
        if not 0 <= percentage_removed_nodes <= 100:
            print(">>> The percentage must be between 0 and 100.\n")
        else:
            break
    
    # the link to load the network graph
    NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

    # parameters for creation of ER and UPA graphs 
    # with characteristics closest to the network graph 
    NUM_NODES = 1239
    PROBABILITY = 0.004
    M_PARAM = 2

    # create three graphs
    netw_graph = load_graph(NETWORK_URL) # 1239 nodes and 3047 edges
    er_graph = er_ugraph(NUM_NODES, PROBABILITY)
    upa_graph = dpa_upa_graph(NUM_NODES, M_PARAM, 'UPA')

    #show the actual number of edges of the graphs
    print ('---------------')
    print ('Number of edges: ER -', compute_num_edges(er_graph))
    print ('Number of edges: UPA -', compute_num_edges(upa_graph))
    print ('Number of edges: network -', compute_num_edges(netw_graph))
    print ('---------------')

    #compute and plot graph resiliences
    plot_resilience(netw_graph, er_graph, upa_graph, attack_type, PROBABILITY, M_PARAM, percentage_removed_nodes)

    print("\n<<< Done >>>\n")


def efficiency():
    '''
    Compares the run times of the functions 
    (fast_targeted_order) and (targeted_order)
    '''
    # get the necessary parameters from user input
    print('\n<<< PARAMETER RETRIEVAL >>>\n')
    while True:
        min_num_nodes = int(input("Choose a minimum number of nodes.\nRecommended value: 10\n"))
        if min_num_nodes < 0:
            print(">>> The minimum number of nodes cannot be negative.\n")
        else:
            break   
    while True:
        max_num_nodes = int(input("Choose a maximum number of nodes.\nRecommended value: 1000\n"))
        if max_num_nodes < min_num_nodes:
            print(">>> The maximum number of nodes cannot be less than the minimum number of nodes.\n")
        else:
            break   
    while True:
        step = int(input("Choose a step of progression.\nRecommended value: 10\n"))
        if step <= 0:
            print(">>> The step has to be a positive number.\n")
        else:
            break 

    #compute and plot the run times of the functions
    plot_efficiency(min_num_nodes, max_num_nodes, step)

    print("\n<<< Done >>>\n")


if __name__ == "__main__":

    analysis_options = {'efficiency': efficiency, 'resilience': resilience}

    # get the type of analysis from user
    while True:
        analysis_choice = input("Do you want to analyze efficiency or resilience?.\nValid entries: 'efficiency' or 'resilience'\n")
        if analysis_choice not in {'efficiency', 'resilience'}:
            print(">>> Invalid choice.\n")
        else:
            break    
    
    # run the chosen analysis function
    analysis_options[analysis_choice]()

