'''
Function for plotting a provided graph distribution, represented as a dictionary.
'''
import matplotlib.pyplot as plt


def plot(dict_norm, dict_log, plot_type, graph_type):

    # sorted by key, return a list of tuples
    if plot_type == 'log':
        lists = sorted(dict_log.items())
    else:
        lists = sorted(dict_norm.items())

    # unpack a list of pairs into two tuples
    x, y = zip(*lists) 
    
    # plot the graph
    plt.plot(x, y)

    # mark 'x' and 'y' axis according to the graph type
    if plot_type == 'log':
        plt.xlabel('log(Number of in-degrees)')
        plt.ylabel('log(Normalized number of occurrences)')
    else:
        plt.xlabel('Number of in-degrees')
        plt.ylabel('Normalized number of occurrences')        
    
    # assign a title
    plt.title(f'{graph_type.capitalize()} graph in-degree distribution')
    
    # exhibit the plot
    plt.show()