import menu
import tkinter as tk
import data_parser as dp
import networkx as nx
import algorithms.genetic_algorithm as ga
import networkx as nx


graph = nx.DiGraph()
dp.graph_establishments(100, graph)
solution = ga.genetic_algorithm(graph, 10, 100, 30, 1)
print(solution)
'''
interface = tk.Tk()
first_page = menu.FirstPage(interface)
interface.mainloop()
'''