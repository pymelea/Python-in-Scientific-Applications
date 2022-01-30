import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def network(ntw: str):
    # Read network
    g = nx.read_edgelist(ntw, create_using = nx.Graph(), nodetype = int)

    # Simple info
    ncc = nx.number_connected_components(g)
    spl = nx.shortest_path_length(g, source = 18122, target = 88, weight = None, method = 'dijkstra')
    print(nx.info(g))
    print(f'Number of connected components: {ncc}')
    print(f'Shortest path length from 18122 to 88: {spl}')

    try:
        aspl = nx.average_shortest_path_length(g, weight=None, method=None)
        print(f'Average shortest path length: {aspl}')
    except nx.exception.NetworkXError:
        print('Graph is not connected.')
        
    degree_sequence = sorted([d for n, d in g.degree()], reverse=True)

    # Create figure
    fig = plt.figure('Degree CA-HepTh', figsize = (8, 8))
    # Create subplots grid 3:2
    axgrid = fig.add_gridspec(3, 2)

    # Plot connected components of network
    ax0 = fig.add_subplot(axgrid[0:2, :])
    ccg = g.subgraph(sorted(nx.connected_components(g), key = len, reverse = True)[0])
    pos = nx.spring_layout(ccg, seed = 1234)
    nx.draw_networkx_nodes(ccg, pos, ax = ax0, node_size = 1, node_color = '#96CC39')
    nx.draw_networkx_edges(ccg, pos, ax = ax0, alpha = 0.1)
    ax0.set_title('Connected components of G', fontname = 'Times New Roman', fontsize = 18)
    ax0.set_axis_off()

    # Degree rank plot
    ax1 = fig.add_subplot(axgrid[2:, :1])
    ax1.grid(color = 'gray', linestyle = '-.', linewidth = 0.5)
    ax1.plot(degree_sequence, linestyle = '-', marker = '.', alpha = 0.65, color = '#96CC39')
    ax1.set_title('Degree Rank Plot', fontname = 'Times New Roman', fontsize = 14)
    ax1.set_ylabel('Degree', fontname = 'Times New Roman', fontsize = 14)
    ax1.set_xlabel('Rank', fontname = 'Times New Roman', fontsize = 14)
    ax1.set_xscale('log')
    #ax1.set_xlim([-30, 2000])

    # Degree histogram
    ax2 = fig.add_subplot(axgrid[2:, 1:])
    ax2.grid(color = 'gray', linestyle = '-.', linewidth = 0.5)
    ax2.bar(*np.unique(degree_sequence, return_counts = True), alpha = 0.65, color = '#96CC39')
    ax2.set_title('Degree Histogram', fontname = 'Times New Roman', fontsize = 14)
    ax2.set_xlabel('Degree', fontname = 'Times New Roman', fontsize = 14)
    ax2.set_ylabel('Nodes', fontname = 'Times New Roman', fontsize = 14)
    ax2.set_xlim([0, 20])

    fig.tight_layout()
    plt.show()


# MAIN
if __name__ == '__main__':
    filename = 'CA-GrQc.txt'
    network(filename)