from math import floor
import networkx as nx
import data_parser as dp
import matplotlib.pyplot as plt
import algorithms.random_algorithm as rs
import algorithms.hill_climbing as hc
import algorithms.simulated_annealing as sa
import algorithms.tabu_search as ts
import utils
import time_utils
from datetime import datetime, timedelta


graph = nx.DiGraph()
n = 1000
aux = floor(0.1*n)
vans = aux if aux>1 else 1
dp.graph_establishments(n, graph)

solution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), vans, 0) # grafo, departure time, número de vans, starting van
# print max de arrival time
print(solution)
print(time_utils.total_time(solution)[1])
#sa_solution = sa.simulated_annealing(graph, solution, 7)

#print(sa_solution)
#print(time_utils.total_time(sa_solution)[1])
#solution = utils.get_random_neighbour(graph, solution)
#print("\n" + str(solution))
hc.hillClimbing(graph,solution,vans)

ts.tabu_search(graph,solution,n)


#print(solution)


if n <0:
    # draw the graph
    pos = nx.spring_layout(graph)  # compute layout


    nx.draw(graph, pos, with_labels=True, font_size = 10, edge_color = 'b')  # draw nodes and edges


    node_labels = nx.get_node_attributes(graph, 'parish')  # get node labels
    nx.draw_networkx_labels(graph, pos, labels=node_labels)  # draw node labels

    edge_labels = nx.get_edge_attributes(graph, 'travelTime')  # get edge labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)  # draw edge labels

    plt.show()  # show the plot'''