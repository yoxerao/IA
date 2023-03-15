from math import floor
import networkx as nx
import data_parser as dp
import matplotlib.pyplot as plt
import algorithms.randomSolution as rs
import algorithms.hillClimbing as hc

graph = nx.Graph()
n = 1000
aux = floor(0.1*n)
k = aux if aux>1 else 1
dp.graph_establishments(n, graph)

solution = rs.calculate_random_paths(graph, k, 0)
hc.hillClimbing(solution)
print(solution)
print("total time: ", max([solution[i][-1][1] for i in range(k)]), "h")

'''if n <20:
    # draw the graph
    pos = nx.spring_layout(graph)  # compute layout


    nx.draw(graph, pos, with_labels=True, font_size = 10, edge_color = 'b')  # draw nodes and edges


    node_labels = nx.get_node_attributes(graph, 'parish')  # get node labels
    nx.draw_networkx_labels(graph, pos, labels=node_labels)  # draw node labels

    edge_labels = nx.get_edge_attributes(graph, 'travelTime')  # get edge labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)  # draw edge labels

    plt.show()  # show the plot'''