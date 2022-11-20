'''

'''


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
    import random
    from copy import deepcopy

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
    from copy import deepcopy

    new_graph = deepcopy(ugraph)
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            node_neigh = new_graph[node]
            if len(node_neigh) > max_degree:
                max_degree = len(node_neigh)
                max_degree_node = node
        
        delete_node (new_graph, max_degree_node)

        order.append(max_degree_node)
    
    return order
    

def random_order(a_graph):
    '''
    Receives graph and returns a randomly shuffled list of its nodes.
    '''
    import random

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


def plot_resilience(netw_graph, er_graph, upa_graph, attack_type, er_prob, upa_m_param, percentage_removed_nodes = 100):
    '''
    Computes and plots the resilience of 3 graphs 
    depending on the (attack_type) used
    '''
    from project_2 import compute_resilience
    import matplotlib.pyplot as plt

    attack_funcs = {'random' : random_order, 'targeted' : fast_targeted_order}

    netw_resilience = compute_resilience(netw_graph, attack_funcs[attack_type](netw_graph))
    er_resilience = compute_resilience(er_graph, attack_funcs[attack_type](er_graph))
    upa_resilience = compute_resilience(upa_graph, attack_funcs[attack_type](upa_graph))

    num_removed_nodes = int(len(netw_resilience) * percentage_removed_nodes / 100)
    x_vals = range(num_removed_nodes)
    y_vals_1 = []
    y_vals_2 = []
    y_vals_3 = []
    for x in x_vals:
        y_vals_1.append(netw_resilience[x])
        y_vals_2.append(er_resilience[x])
        y_vals_3.append(upa_resilience[x])

    plt.title(f'Comparing resilience between graphs\n({attack_type} attack)')
    plt.xlabel(f'Number of nodes removed (up to {percentage_removed_nodes}%)')
    plt.ylabel('Size of the largest connected component')  
    
    plt.plot(x_vals, y_vals_1, '-b', label = 'Computer network')
    plt.plot(x_vals, y_vals_2, '-r', label = f'ER (prob. = {er_prob})')
    plt.plot(x_vals, y_vals_3, '-g', label = f'UPA (m_param = {upa_m_param})')
    plt.legend(loc='upper right')
    plt.savefig(f'{attack_type}_attack_resilience({percentage_removed_nodes}%).png')
    plt.show()


def fast_vs_brute(num_nodes, m_param):
    '''
    Computes the running times for (targeted_order)
    and (fast_targeted_order) functions applied to
    a random-generated UPA graph with (num_nodes) and (m_param)
    '''
    from dpa_upa_graph_gen import dpa_upa_graph
    from timeit import default_timer as timer

    a_graph = dpa_upa_graph (num_nodes, m_param, 'UPA')

    start = timer()
    _ = fast_targeted_order(a_graph)
    end = timer()
    fast_time = end - start

    start = timer()
    _ = targeted_order(a_graph)
    end = timer()    
    brute_time = end - start

    return fast_time, brute_time


def plot_efficiency(min_num_nodes, max_num_nodes, step, m_param = 5):
    '''
    Computes and plots the efficiency of (fast_targeted_order)
    and (targeted_order), as a function of running time and the
    size of a processed graph.
    '''
    import matplotlib.pyplot as plt

    x_vals = []
    y_vals_fast = []
    y_vals_brute = []
    for num_nodes in range(min_num_nodes, max_num_nodes, step):
        x_vals.append(num_nodes)
        run_times = fast_vs_brute(num_nodes, m_param)
        y_vals_fast.append(run_times[0])
        y_vals_brute.append(run_times[1])
    
    plt.title('(fast_targeted_order) and (targeted_order) efficiency comparison\nDesktop Python')
    plt.xlabel('Number of nodes')
    plt.ylabel('Running time')  
    
    plt.plot(x_vals, y_vals_fast, '-b', label = 'Fast')
    plt.plot(x_vals, y_vals_brute, '-r', label = 'Brute force')
    plt.legend(loc = 'upper left', title = f'({min_num_nodes}, {max_num_nodes}, {step})\nm_param = {m_param}')
    plt.savefig(f'efficiency_comparison_{max_num_nodes}.png')
    plt.show()


def main():
    '''
    The main script
    '''
    from application_1 import load_graph
    from er_graph_gen import er_ugraph
    from dpa_upa_graph_gen import dpa_upa_graph

    NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
    NUM_NODES = 1239
    PROBABILITY = 0.004
    M_PARAM = 2

    netw_graph = load_graph(NETWORK_URL) # 1239 nodes and 3047 edges
    er_graph = er_ugraph(NUM_NODES, PROBABILITY)
    upa_graph = dpa_upa_graph(NUM_NODES, M_PARAM, 'UPA')

    print ('')
    print ('Number of edges: ER -', compute_num_edges(er_graph))
    print ('Number of edges: UPA -', compute_num_edges(upa_graph))
    print ('Number of edges: network -', compute_num_edges(netw_graph))
    print('')

    plot_resilience(netw_graph, er_graph, upa_graph, 'targeted', PROBABILITY, M_PARAM, 20)
    #plot_efficiency(10, 1000, 10)

    print("<<< DONE >>>")


if __name__ == "__main__":
    main()

