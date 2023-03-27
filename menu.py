import tkinter as tk
from tkinter import messagebox

class FirstPage:
    def __init__(self, master):
        self.master = master
        self.master.title("First Page")
        self.master.geometry("500x400")
        
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


class MainMenu:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Main Menu")
        self.master.geometry("500x400")
        
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
        self.confirm_button = tk.Button(self.master, text="OK", command=self.confirm)
        self.confirm_button.pack(pady=20)
        
        self.master.mainloop()
        
    def confirm(self):
        # check if number input is valid and in range
        n_establishments = self.input_n_est.get()
        while True:
            n_establishments = self.input_n_est.get()
            if not n_establishments.isdigit() or int(n_establishments) < 2 or int(n_establishments) > 1000:
                tk.messagebox.showerror("Error", "Enter a valid input")
                self.input_n_est.delete(0, tk.END)
                self.input_n_est.focus()
            else:
                n_establishments = int(n_establishments)
                break

        # check chosen algorithm
        chosen_algorithm = self.chosen_algorithm.get()
        if chosen_algorithm is None:
            tk.messagebox.showerror("Error", "Select an algorithm")
            self.chosen_algorithm.delete(0, tk.END)
            chosen_algorithm = self.chosen_algorithm.get()
            
        if chosen_algorithm == "Random":
            self.master.destroy()
            MenuRandom()
        elif chosen_algorithm == "Hill Climbing":
            self.master.destroy()
            MenuHillClimbing()
        elif chosen_algorithm == "Simulated Annealing":
            self.master.destroy()
            MenuSimulatedAnnealing()
        elif chosen_algorithm == "Tabu Search":
            self.master.destroy()
            MenuTabuSearch()
        elif chosen_algorithm == "Genetic Algorithm":
            self.master.destroy()
            MenuGeneticAlgorithm()


class MenuBase:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x400")

        # exit to main menu button
        exit_button = tk.Button(self.master, text="Exit", command=self.exit_main_menu)
        exit_button.pack(side="bottom")

    def exit_main_menu(self):
        self.master.destroy()
        MainMenu()


class MenuRandom(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Random Algorithm")


class MenuHillClimbing(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Hill Climbing")


class MenuSimulatedAnnealing(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Simulated Annealing")
    
 
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