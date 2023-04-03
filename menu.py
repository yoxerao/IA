import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import time

import data_parser as dp

import algorithms.random_algorithm as rs
import algorithms.hill_climbing as hc
import algorithms.simulated_annealing as sa
import algorithms.tabu_search as ts

import utils
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
        
        # chose algorithm questoin
        self.algorithm = tk.Label(self.master, text="Chose an algorithm:")
        self.algorithm.pack(pady=10)
        self.chosen_algorithm = tk.StringVar()
        self.chosen_algorithm.set(None)
        algorithms = ["Random", "Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"]
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


        match algorithm:
            case "Random":
                MenuRandom(self.master, n_vans, n_establishments, graph).mainloop()
            case "Hill Climbing":
                MenuHillClimbing(self.master, n_vans, n_establishments, graph).mainloop()
            case "Simulated Annealing":
                MenuSimulatedAnnealing(self.master, n_vans, n_establishments, graph).mainloop()
            case "Tabu Search":
                MenuTabuSearch(self.master, n_vans, n_establishments, graph).mainloop()
            case "Genetic Algorithm":
                MenuGeneticAlgorithm(self.master, n_vans, n_establishments, graph).mainloop()
            case _:
                tk.messagebox.showerror("Error", "Please enter a valid number of establishments and choose an algorithm.")
        '''if algorithm == "Hill Climbing":
            MenuHillClimbing(self.master, n_establishments).mainloop()'''
        
        '''elif algorithm == "Tabu Search":f
            self.master.destroy()
            MenuTabuSearch()
        elif algorithm == "Genetic Algorithm":
            self.master.destroy()
            MenuGeneticAlgorithm()'''
        

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
        
        solution_graph = utils.graph_solution(solution, graph)
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Solution Graph\n\n Total Travel Time (h.m.s): " + time_utils.total_time(solution)[1])

        pos = nx.spring_layout(solution_graph)
       
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
        self.master.title("Menu Random")
        self.master.geometry("400x340")
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
        self.solution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)
        if self.graph_option.get() == 1:
            self.display_solution_graph(graph, self.solution)


class MenuHillClimbing(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.master.geometry("400x350")
        self.master.title("Menu Hill Climbing")
        self.title = tk.Label(self, text="Hill Climbing", font=("Arial", 12))
        self.title.pack(pady=10)
        
        self.question = tk.StringVar()
        self.question.set("Which type of neighbourhoods do you want to use?")
        self.label_question = tk.Label(self, textvariable=self.question)
        self.label_question.pack()
        
        self.neighbourhood1 = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(self, text="Neighbourhood 1", variable=self.neighbourhood1)
        self.checkbox1.pack()
        self.neighbourhood2 = tk.IntVar()
        self.checkbox2 = tk.Checkbutton(self, text="Neighbourhood 2", variable=self.neighbourhood2)
        self.checkbox2.pack()
        self.neighbourhood3 = tk.IntVar()
        self.checkbox3 = tk.Checkbutton(self, text="Neighbourhood 3", variable=self.neighbourhood3)
        self.checkbox3.pack()
        
        self.run_button = tk.Button(self, text="Run", command=self.check_input)
        self.run_button.pack()


        
    def check_input(self):
        neighbourhoods = [self.neighbourhood1.get(), self.neighbourhood2.get(), self.neighbourhood3.get()]
        
        try:
            if all(val == 0 for val in neighbourhoods):
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Please select at least one neihgbourhood.")
            return False
        

class MenuSimulatedAnnealing(MenuBase):
    def __init__(self, master, n_vans, n_establishments, graph):
        super().__init__(master)
        self.master.title("Menu Simulated Annealing")
        self.geometry("600x400")
        self.solution = None

        input_label = tk.Label(self, text="Cooling factor (lower values = faster cooling, values between 5 and 7 recommended):")
        input_label.pack()
        self.input_entry = tk.Entry(self)
        self.input_entry.pack(pady=10)

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
        self.rsolution = rs.calculate_random_paths(graph, time_utils.seconds_to_string(9*3600), n_vans, 0)
        start_time = time.time()
        self.solution = sa.simulated_annealing(graph, self.rsolution, float(cooling_factor))
        end_time = time.time()
        execution_time = end_time - start_time
        input_label = tk.Label(self, text="Solution found, check console for full solution")
        input_label.pack()

        input_label = tk.Label(
            self, 
            text="Final arrival time (h.m.s):" + time_utils.total_time(self.solution)[1] + "\n Execution time (h.m.s): " + time_utils.seconds_to_string(execution_time), 
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
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Tabu Search")


class MenuGeneticAlgorithm(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Genetic Algorithm")


interface = tk.Tk()
first_page = FirstPage(interface)
interface.mainloop()

