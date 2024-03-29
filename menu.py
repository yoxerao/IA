import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import time
import time_utils
import networkx as nx

import data_parser as dp

import algorithms.random_algorithm as rs
import algorithms.hill_climbing as hc
import algorithms.simulated_annealing as sa
import algorithms.tabu_search as ts
import algorithms.genetic_algorithm as ga

import time_utils

from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from math import floor

class FirstPage:
    def __init__(self, master):
        self.master = master
        self.master.title("First Page")
        self.master.geometry("400x350")
        
        # title widget
        self.title = tk.Label(self.master, text="Travel Time Minimization", font=("Arial", 24))
        self.title.pack(pady=50)
        
        # go to menu widget
        self.instruction = tk.Label(self.master, text="Tap anywhere to continue", font=("Arial", 10))
        self.instruction.pack(pady=20)
        
        # add event to go to main menu
        self.master.bind("<Button-1>", self.go_to_main_menu)
        
    def go_to_main_menu(self, event):
        self.master.unbind("<Button-1>")
        self.master.destroy()
        MainMenu().master.mainloop()


class MainMenu(tk.Toplevel):
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Main Menu")
        self.master.geometry("400x340")
        self.title = tk.Label(self.master, text="Menu", font=("Arial", 12))
        self.title.pack(pady=10)

        
        # number of establishments question
        self.n_establishments = tk.Label(self.master, text="Enter the number of establishments (between 2 and 1000): ")
        self.n_establishments.pack(pady=10)
        self.input_n_est = tk.Entry(self.master)
        self.input_n_est.pack()
        
        # chose algorithm question
        self.algorithm = tk.Label(self.master, text="Chose an algorithm:")
        self.algorithm.pack(pady=10)
        self.chosen_algorithm = tk.StringVar()
        self.chosen_algorithm.set(None)
        algorithms = ["Random", "Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"]

        self.rsolution_shared = None
        for a in algorithms:
            radio = tk.Radiobutton(self.master, text=a, variable=self.chosen_algorithm, value=a)
            radio.pack()
        
        # confirm button
        self.confirm_button = tk.Button(self.master, text="OK", command=self.check_input)
        self.confirm_button.pack(pady=20)
        
        self.master.mainloop()

    def check_input(self):

        try:
            n = int(self.input_n_est.get())
            if n < 2 or n > 1000:
                raise ValueError
            algorithm = self.chosen_algorithm.get()
            if algorithm is None:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of establishments and choose an algorithm.")
            return False
        
        graph = nx.DiGraph()
        n_establishments = int(self.input_n_est.get())
        aux = floor(0.1*n_establishments)
        n_vans = aux if aux>1 else 1
        dp.graph_establishments(n, graph)

        if self.rsolution_shared is None:
            self.rsolution_shared = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)

        match algorithm:
            case "Random":
                MenuRandom(self.master, n_vans, n_establishments, graph).mainloop()
            case "Hill Climbing":
                MenuHillClimbing(self.master, n_vans, n_establishments, graph, self.rsolution_shared).mainloop()
            case "Simulated Annealing":
                MenuSimulatedAnnealing(self.master, n_vans, n_establishments, graph, self.rsolution_shared).mainloop()
            case "Tabu Search":
                MenuTabuSearch(self.master, n_vans, n_establishments, graph, self.rsolution_shared).mainloop()
            case "Genetic Algorithm":
                MenuGeneticAlgorithm(self.master, n_vans, n_establishments, graph).mainloop()
            case _:
                tk.messagebox.showerror("Error", "Please enter a valid number of establishments and choose an algorithm.")
        

class MenuBase(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.geometry("400x340")
        # exit to main menu button
        exit_button = tk.Button(self, text="Main Menu", command=self.exit_to_main_menu)
        exit_button.pack(side="bottom")

    def display_solution_graph(self, graph, solution):
        label = tk.Label(self, text="Use the toolbar on the bottom left to zoom in/out and move the graph")
        label.pack(pady = 10)
        
        solution_graph = graph_solution(solution, graph)
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Solution Graph\n\n Total Travel Time (h.m.s): " + time_utils.total_time(solution))

        scale = 0.4
        pos = {node: (time_utils.string_to_seconds(data['arrival_time']), i*scale) for i, (node, data) in enumerate(solution_graph.nodes(data=True))}
       
        arrival_times = {node: data.get('arrival_time', '') for node, data in solution_graph.nodes(data=True)}

        node_labels = {node: f"{node}\nArrival: {arrival_times[node]}" for node in solution_graph.nodes}
        edge_labels = {(u, v): d["travel_time"] for u, v, d in solution_graph.edges(data=True)}

        path_colors = {i: plt.cm.tab10(i) for i in range(10)}
        edge_colors = [path_colors[d['van']] for u, v, d in solution_graph.edges(data=True)]
    
        nx.draw(solution_graph, pos, ax=ax, with_labels=True, node_color="lightblue", edge_color=edge_colors, width=2, labels = node_labels)
        nx.draw_networkx_edge_labels(solution_graph, pos, edge_labels=edge_labels, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    def exit_to_main_menu(self):
        self.master.destroy()
        MainMenu().master.mainloop()
        
class MenuRandom(MenuBase):
    def __init__(self, master, n_vans, n_establishments, graph):
        super().__init__(master)
        self.title("Menu Random")
        self.geometry("400x340")
        self.solution = None
        self.graph_option = tk.IntVar()

        if(n_establishments <= 100):
            self.checkbox1 = tk.Checkbutton(self, text="Display graph", variable=self.graph_option)
            self.checkbox1.pack()
        else:
            label = tk.Label(self, text="Displaying the solution graph is only available if there are less than 101 establishments",foreground="red", background="black")
            label.pack(pady = 10)
            self.graph_option.set(0)

        self.run_button = tk.Button(self, text="Get Random Solution", command=lambda: self.calculate_random_paths(n_vans, graph))
        self.run_button.pack(pady=10)
        

    def calculate_random_paths(self, n_vans, graph):
        start_time = time.time()
        self.solution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)
        end_time = time.time()
        execution_time = end_time - start_time

        final_time = time_utils.total_time(self.solution)

        input_label = tk.Label(self, text="Solution found, check console for full solution")
        input_label.pack()
        
        print ("Final arrival time (h.m.s): " + final_time)
        print ("Execution time (s): " + str(execution_time))
        input_label = tk.Label(
            self, 
            text="Final arrival time (h.m.s): " + final_time
                + "\nExecution time (s): " + str(execution_time), 
            font=("Arial", 12, "bold"), 
            foreground="white", 
            background="grey", 
            pady=10, 
            relief="solid", 
            borderwidth=2
        )
        input_label.pack()

        if self.graph_option.get() == 1:
            self.display_solution_graph(graph, self.solution)
        



class MenuHillClimbing(MenuBase):
    def __init__(self, master, n_vans, n_establishments, graph, rsolution_shared):
        super().__init__(master)
        self.title("Menu Hill Climbing")
        self.geometry("400x340")
        self.solution = None
        
        self.rsolution_shared = rsolution_shared
        self.shared_random_option = tk.IntVar()
        self.checkbox0 = tk.Checkbutton(self, text="Use preloaded random", variable=self.shared_random_option)
        self.checkbox0.pack()

        self.graph_option = tk.IntVar()
        if(n_establishments <= 100):
            self.checkbox1 = tk.Checkbutton(self, text="Display graph", variable=self.graph_option)
            self.checkbox1.pack()
        else:
            label = tk.Label(self, text="Displaying the solution graph is only available if there are less than 101 establishments",foreground="red", background="black")
            label.pack(pady = 10)
            self.graph_option.set(0)

        self.run_button = tk.Button(self, text="Get HC Solution", command=lambda: self.calculate_hc_solution(n_vans, graph))
        self.run_button.pack(pady=10)


    def calculate_hc_solution(self, n_vans, graph):
        print(self.shared_random_option.get())
        print(self.rsolution_shared)
        if self.shared_random_option.get() == 1:
            self.rsolution = self.rsolution_shared
        else:
            self.rsolution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)
        start_time = time.time()
        self.solution = hc.hillClimbing(graph, self.rsolution)
        end_time = time.time()
        execution_time = end_time - start_time

        random_time = time_utils.total_time(self.rsolution)
        final_time = time_utils.total_time(self.solution)

        improvement = (time_utils.string_to_seconds(random_time) - time_utils.string_to_seconds(final_time)) / time_utils.string_to_seconds(random_time) * 100

        input_label = tk.Label(self, text="Solution found, check console for full solution")
        input_label.pack()

        print ("Random arrival time (h.m.s): " + random_time)
        print ("Final arrival time (h.m.s): " + final_time)
        print ("Improvement: " + str(round(improvement, 2)) + "%")
        print ("Execution time (s): " + str(execution_time))

        input_label = tk.Label(
            self, 
            text="Random arrival time (h.m.s): " + random_time
                + "\nFinal arrival time (h.m.s): " + final_time
                + "\nImprovement: " + str(round(improvement, 2)) + "%"
                + "\nExecution time (h.m.s): " + str(execution_time), 
            font=("Arial", 12, "bold"), 
            foreground="white", 
            background="grey", 
            pady=10, 
            relief="solid", 
            borderwidth=2
        )
        input_label.pack()

        if self.graph_option.get() == 1:
            self.display_solution_graph(graph, self.solution)

    def check_input(self):
        neighbourhoods = [self.neighbourhood1.get(), self.neighbourhood2.get(), self.neighbourhood3.get()]
        
        try:
            if all(val == 0 for val in neighbourhoods):
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Please select at least one neihgbourhood.")
            return False
        

class MenuSimulatedAnnealing(MenuBase):
    def __init__(self, master, n_vans, n_establishments, graph, rsolution_shared):
        super().__init__(master)
        self.title("Menu Simulated Annealing")
        self.geometry("600x400")
        self.solution = None

        input_label = tk.Label(self, text="Cooling factor (lower values = faster cooling, values between 5 and 7 recommended):")
        input_label.pack()
        self.input_entry = tk.Entry(self)
        self.input_entry.insert(0, "5")
        self.input_entry.pack(pady=10)

        self.rsolution_shared = rsolution_shared
        self.shared_random_option = tk.IntVar()
        self.checkbox0 = tk.Checkbutton(self, text="Use preloaded random", variable=self.shared_random_option)
        self.checkbox0.pack()

        self.graph_option = tk.IntVar()
        if(n_establishments <= 100):
            self.checkbox1 = tk.Checkbutton(self, text="Display graph", variable=self.graph_option)
            self.checkbox1.pack()
        else:
            label = tk.Label(self, text="Displaying the solution graph is only available if there are less than 101 establishments",foreground="red", background="black")
            label.pack(pady = 10)
            self.graph_option.set(0)

        self.run_button = tk.Button(self, text="Get SA Solution", command=lambda: self.calculate_sa_solution(n_vans, graph, self.input_entry.get()))
        self.run_button.pack(pady=10)

        note_label = tk.Label(self, text="Generating a solution will take a while... \n Check the console for info while generating.")
        note_label.pack(pady=10)


    def calculate_sa_solution(self, n_vans, graph, cooling_factor):
        if self.shared_random_option.get() == 1:
            self.rsolution = self.rsolution_shared
        else:
            self.rsolution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)

        start_time = time.time()
        self.solution = sa.simulated_annealing(graph, self.rsolution, float(cooling_factor))
        end_time = time.time()
        execution_time = end_time - start_time

        input_label = tk.Label(self, text="Solution found, check console for full solution")
        input_label.pack()
        
        random_time = time_utils.total_time(self.rsolution)
        final_time = time_utils.total_time(self.solution)

        improvement = (time_utils.string_to_seconds(random_time) - time_utils.string_to_seconds(final_time)) / time_utils.string_to_seconds(random_time) * 100

        print ("Random arrival time (h.m.s): " + random_time)
        print ("Final arrival time (h.m.s): " + final_time)
        print ("Improvement: " + str(round(improvement, 2)) + "%")
        print ("Execution time (s): " + str(execution_time))
        input_label = tk.Label(
            self, 
            text="Random arrival time (h.m.s): " + random_time
                + "\nFinal arrival time (h.m.s): " + final_time
                + "\nImprovement: " + str(round(improvement, 2)) + "%"
                + "\nExecution time (h.m.s): " + str(execution_time), 
            font=("Arial", 12, "bold"), 
            foreground="white", 
            background="grey", 
            pady=10, 
            relief="solid", 
            borderwidth=2
        )
        input_label.pack()

        if self.graph_option.get() == 1:
            self.display_solution_graph(graph, self.solution)
    
 
class MenuTabuSearch(MenuBase):
    def __init__(self, master, n_vans, n_establishments, graph, rsolution_shared):
        super().__init__(master)
        self.title("Menu Tabu Search")
        self.geometry("600x400")
        self.solution = None

        input_label = tk.Label(self, text="Number of iterations:")
        input_label.pack()
        self.n_iterations = tk.Entry(self)
        self.n_iterations.insert(0, "1000")
        self.n_iterations.pack()

        input_label = tk.Label(self, text="Mutations per iteration:")
        input_label.pack()
        self.n_mutations = tk.Entry(self)
        self.n_mutations.insert(0, "150")
        self.n_mutations.pack()

        self.rsolution_shared = rsolution_shared
        self.shared_random_option = tk.IntVar()
        self.checkbox0 = tk.Checkbutton(self, text="Use preloaded random", variable=self.shared_random_option)
        self.checkbox0.pack()

        self.graph_option = tk.IntVar()
        if(n_establishments <= 100):
            self.checkbox1 = tk.Checkbutton(self, text="Display graph", variable=self.graph_option)
            self.checkbox1.pack()
        else:
            label = tk.Label(self, text="Displaying the solution graph is only available if there are less than 101 establishments",foreground="red", background="black")
            label.pack(pady = 10)
            self.graph_option.set(0)

        self.run_button = tk.Button(self, text="Get TS Solution", command=lambda: self.calculate_ts_solution(n_establishments, n_vans, graph, self.n_iterations.get(), self.n_mutations.get()))
        self.run_button.pack(pady=10)

        note_label = tk.Label(self, text="Generating a solution will take a while... \n Check the console for info while generating.")
        note_label.pack(pady=10)


    def calculate_ts_solution(self, n_establishments, n_vans, graph, n_iterations, n_mutations):
        
        if self.shared_random_option.get() == 1:
            self.rsolution = self.rsolution_shared
        else:
            self.rsolution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)

        start_time = time.time()
        self.solution = ts.tabu_search(graph, self.rsolution, n_establishments, int(n_iterations), int(n_mutations))
        end_time = time.time()
        execution_time = end_time - start_time

        input_label = tk.Label(self, text="Solution found, check console for full solution")
        input_label.pack()
        
        random_time = time_utils.total_time(self.rsolution)
        final_time = time_utils.total_time(self.solution)

        improvement = (time_utils.string_to_seconds(random_time) - time_utils.string_to_seconds(final_time)) / time_utils.string_to_seconds(random_time) * 100

        print ("Random arrival time (h.m.s): " + random_time)
        print ("Final arrival time (h.m.s): " + final_time)
        print ("Improvement: " + str(round(improvement, 2)) + "%")
        print ("Execution time (s): " + str(execution_time))
        input_label = tk.Label(
            self, 
            text="Random arrival time (h.m.s): " + random_time
                + "\nFinal arrival time (h.m.s): " + final_time
                + "\nImprovement: " + str(round(improvement, 2)) + "%"
                + "\nExecution time (h.m.s): " + str(execution_time), 
            font=("Arial", 12, "bold"), 
            foreground="white", 
            background="grey", 
            pady=10, 
            relief="solid", 
            borderwidth=2
        )
        input_label.pack()

        if self.graph_option.get() == 1:
            self.display_solution_graph(graph, self.solution)

class MenuGeneticAlgorithm(MenuBase):
    def __init__(self, master, n_vans, n_establishments, graph):
        super().__init__(master)
        self.title("Menu Genetic Algorithm")
        self.geometry("600x400")
        self.solution = None

        input_label = tk.Label(self, text="Number of generations: ")
        input_label.pack()
        self.n_generations = tk.Entry(self)
        self.n_generations.insert(0, "100")
        self.n_generations.pack()

        input_label = tk.Label(self, text="Mutation probability (between 0 and 100): ")
        input_label.pack()
        self.mutation_prob = tk.Entry(self)
        self.mutation_prob.insert(0, "20")
        self.mutation_prob.pack()
        
        self.mutation_types = tk.Label(self, text="Mutation type:")
        self.mutation_types.pack()
        self.chosen_mutation_type = tk.StringVar()
        self.chosen_mutation_type.set("Swap mutation (random)")
        mutation_types = ["Swap mutation (random)", "Tabu Search"]
        for a in mutation_types:
            radio = tk.Radiobutton(self, text=a, variable=self.chosen_mutation_type, value=a)
            radio.pack()

        self.graph_option = tk.IntVar()
        if(n_establishments <= 100):
            self.checkbox1 = tk.Checkbutton(self, text="Display graph", variable=self.graph_option)
            self.checkbox1.pack()
        else:
            label = tk.Label(self, text="Displaying the solution graph is only available if there are less than 101 establishments",foreground="red", background="black")
            label.pack(pady = 10)
            self.graph_option.set(0)

        self.run_button = tk.Button(self, text="Get GA Solution", command=lambda: self.check_input() and self.calculate_ga_solution(n_establishments, n_vans, graph, self.n_generations.get(), self.mutation_prob.get(), self.chosen_mutation_type.get()))
        self.run_button.pack(pady=10)

        note_label = tk.Label(self, text="Generating a solution will take a while... \n Check the console for info while generating.")
        note_label.pack(pady=10)
    
    def check_input(self):
        try:
            n1 = int(self.n_generations.get())
            n2 = int(self.mutation_prob.get())
            mutation_type = self.chosen_mutation_type.get()
            if mutation_type is None:
                raise ValueError
            if n2 < 0 or n2 > 100:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of generations and mutation probability.")
            return False
        return True


    def calculate_ga_solution(self, n_establishments, n_vans, graph, n_generations, mutation_prob, mutation_type):
        start_time = time.time()
        match mutation_type:
            case "Swap mutation (random)":
                mutation_type = 0
            case "Tabu Search":
                mutation_type = 1
        self.solution, self.first_parent, self.second_parent = ga.genetic_algorithm(graph, n_vans, n_establishments, int(n_generations), int(mutation_prob)/100, mutation_type)
        end_time = time.time()
        execution_time = end_time - start_time

        input_label = tk.Label(self, text="Solution found, check console for full solution")
        input_label.pack()
        
        first_parent_time = time_utils.total_time(self.first_parent)
        second_parent_time = time_utils.total_time(self.second_parent)
        final_time = time_utils.total_time(self.solution)
        
        med_parents = (time_utils.string_to_seconds(first_parent_time) + time_utils.string_to_seconds(second_parent_time)) / 2

        improvement = (med_parents - time_utils.string_to_seconds(final_time)) / med_parents * 100

        print ("First Parent arrival time (h.m.s): " + first_parent_time)
        print ("Second Parent arrival time (h.m.s): " + second_parent_time)
        print ("Final arrival time (h.m.s): " + final_time)
        print ("Improvement: " + str(round(improvement, 2)) + "%")
        print ("Execution time (s): " + str(execution_time))
        input_label = tk.Label(
            self, 
            text="First Parent arrival time (h.m.s): " + first_parent_time
                + "\nSecond Parent arrival time (h.m.s): " + second_parent_time
                + "\nFinal arrival time (h.m.s): " + final_time
                + "\nImprovement: " + str(round(improvement, 2)) + "%"
                + "\nExecution time (h.m.s): " + str(execution_time), 
            font=("Arial", 12, "bold"), 
            foreground="white", 
            background="grey", 
            pady=10, 
            relief="solid", 
            borderwidth=2
        )
        input_label.pack()

        if self.graph_option.get() == 1:
            self.display_solution_graph(graph, self.solution)  


def graph_solution(solution, graph):
    # create empty graph
    solution_graph = nx.DiGraph()

    # add nodes to graph
    for path in solution:
        for node in path:
            node_index, arrival_time = node
            solution_graph.add_node(node_index, arrival_time=arrival_time)
    solution_graph.add_node(node_index, arrival_time=time_utils.total_time(solution))

    # add edges to graph
    van = 0
    for path in solution:
        for i in range(len(path) - 1):
            currentNode = path[i][0]
            nextNode = path[i + 1][0]
            travel_time = (graph.edges[currentNode, nextNode]['travelTime'])
            solution_graph.add_edge(currentNode, nextNode, travel_time=travel_time, van=van)
        van += 1

    return solution_graph
