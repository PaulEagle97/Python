"""
This is a set of functions for analyzing the resilience of computer networks, 
modeled by graphs, which are represented using dictionaries
"""
from collections import deque
from copy import deepcopy


def bfs_visited(ugraph, start_node):
    """
    Performs a breadth-first search in graph 'ugraph' 
    starting at 'start_node' node.
    Returns a set of all visited nodes.
    """
    queue = deque()
    visited = {start_node}
    queue.append(start_node)
    while len(queue) != 0:
        curr_node = queue.pop()
        for neigh in ugraph[curr_node]:
            if neigh not in visited:
                visited.add(neigh)
                queue.appendleft(neigh)
    
    return visited


def cc_visited(ugraph):
    """
    Takes the undirected graph 'ugraph' and returns a list of sets, 
    where each set consists of all the nodes in a connected component of the graph
    """
    rem_nodes = set(ugraph.keys())
    con_comp = []
    while len(rem_nodes) > 0:
        curr_node = rem_nodes.pop()
        curr_network = bfs_visited(ugraph, curr_node)
        con_comp.append(curr_network)
        rem_nodes.difference_update(curr_network)
    
    return con_comp


def largest_cc_size(ugraph):
    """
    Returns the size of the largest connected component 
    in 'ugraph' graph
    """
    con_comp = cc_visited(ugraph)
    larg_comp = {}
    for comp in con_comp:
        if len(comp) > len(larg_comp):
            larg_comp = comp.copy()
    
    return len(larg_comp)
    

def compute_resilience(ugraph, attack_order):
    """
    Computes a list of values of a largest connected component of a (ugraph) graph
    after the sequential removal of nodes from (attack_order) list
    """
    a_graph = deepcopy(ugraph)
    cc_size_lst = [largest_cc_size(a_graph)]
    for node in attack_order:
        removed_edges = a_graph.pop(node, "No node found")
        for con_node in removed_edges:
            a_graph[con_node].difference_update({node})
        cc_size_lst.append(largest_cc_size(a_graph))
    
    return cc_size_lst


def test():
    '''
    Testing functions
    '''
    print('\n<<< TEST START >>>\n')

    #creating simple graphs for testing
    EX_GRAPH_DIR = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), \
                3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), \
                7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7]), \
                10: set([]), 11: set([10, 12]), 12: set([10]), 13: set([11])}

    EX_GRAPH_UNDIR = {0: set([1, 3, 4, 5]), 1: set([0, 2, 4, 6]), 2: set([1, 3, 5]), \
                    3: set([0, 2]), 4: set([0, 1]), 5: set([0, 2]), 6: set([1]), \
                    7: set([8, 9]), 8: set([7, 9, 11]), 9: set([7, 8, 10]), \
                    10: set([9, 11]), 11: set([8, 10])}

    # <<< bfs_visited >>> - PASS
    print('bfs_visited function:')
    print (bfs_visited(EX_GRAPH_DIR, 8))
    # expected: {1, 2, 3, 6, 7, 8}
    print (bfs_visited(EX_GRAPH_UNDIR, 7), '\n')
    # expected: {7, 8, 9, 10, 11}

    # <<< cc_visited >>> - PASS
    print ('cc_visited function:')
    print (cc_visited(EX_GRAPH_UNDIR), '\n')
    # expected: [{0, 1, 2, 3, 4, 5, 6}, {7, 8, 9, 10, 11}]

    # <<< largest_cc_size >>> - PASS
    print ('largest_cc_size function:')
    print (largest_cc_size(EX_GRAPH_UNDIR), '\n')
    # expected: 7

    # <<< compute_resilience >>> - PASS
    print ('compute_resilience function:')
    print (compute_resilience(EX_GRAPH_UNDIR, [0, 9, 1, 2, 8]), '\n')
    # expected: [7, 6, 6, 4, 4, 2]

    print('<<< TEST END >>>\n')


if __name__ == "__main__":
    test()

