'''
Functions and classes for generating random DPA/UPA graphs
'''
import random


class Trial:
    """
    Simple class to encapsulate optimized trials for DPA/UPA algorithms
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes, graph_type):
        """
        Initialize a Trial object corresponding to a 
        complete graph with num_nodes nodes
        
        Initial list of node numbers has num_nodes copies of
        each node number
        """
        if graph_type not in {'DPA', 'UPA'}:
            raise ValueError(f'Incorrect graph type provided = {graph_type}')
        elif num_nodes < 0:
            raise ValueError(f'Invalid "m_parameter" provided = {num_nodes}')

        self._graph_type = graph_type
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        if self._graph_type == 'DPA':
            self._node_numbers.append(self._num_nodes)
            self._node_numbers.extend(list(new_node_neighbors))

        elif self._graph_type == 'UPA':
            self._node_numbers.append(self._num_nodes)
            for dummy_idx in range(len(new_node_neighbors)):
                self._node_numbers.append(self._num_nodes)
            self._node_numbers.extend(list(new_node_neighbors))      

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
        

def dpa_upa_graph(num_nodes, m_param, graph_type):
    '''
    Creates a (graph_type) graph using the Trial class.
    Returns the new graph as a dictionary.
    '''
    #initialize and check for an empty graph input
    if num_nodes <= 0:
        raise ValueError(f'Invalid number of nodes provided = {num_nodes}')

    graph = {}
    #create a complete graph with m_param nodes
    #and a helper object for computing neighbors
    all_nodes = set(range(m_param))
    for node in all_nodes:
        graph[node] = all_nodes.difference(set([node]))
    
    graph_obj = Trial(m_param, graph_type)
    #main loop
    for new_node in range(m_param, num_nodes):
        neighbors = graph_obj.run_trial(m_param)
        graph[new_node] = neighbors
        if graph_type == 'UPA':
            for neighbor in neighbors:
                graph[neighbor].update({new_node})
            
    return graph


def test():
    '''
    Creates a sample graph of a certain type, with adjustable parameters,
    and then plots it on a normal or log/log scale.
    '''
    from application_1 import in_degree_distribution, convert_to_log
    import matplotlib.pyplot as plt

    NUM_NODES = 27000
    M_PARAM = 12
    PLOT_TYPE = ''
    GRAPH_TYPE = 'UPA'
    a_graph = dpa_upa_graph(NUM_NODES, M_PARAM, GRAPH_TYPE)

    #compute in-degree distribution and duplicate it
    #on a log/log scale    
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
    
    plt.title(f'{GRAPH_TYPE} graph in-degree distribution')
    
    plt.show()

    print('<<< DONE >>>')


def test_2():
    from project_2 import compute_resilience
    from application_2 import random_order

    upa_graph = dpa_upa_graph(20, 3, 'UPA')
    print(upa_graph, '\n')

    #attack_order = random_order(upa_graph)
    #print (attack_order)

    #upa_resilience = compute_resilience(upa_graph, attack_order)
    #print(upa_resilience)


if __name__ == '__main__':
    test_2()

