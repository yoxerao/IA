import tkinter as tk
from tkinter import messagebox

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
        
        
        n_establishments = int(self.input_n_est.get())
        
        #if algorithm == "Random":
            # chamar random
        if algorithm == "Hill Climbing":
            MenuHillClimbing(self.master).mainloop()
        '''elif algorithm == "Simulated Annealing":
            self.master.destroy()
            MenuSimulatedAnnealing()
        elif algorithm == "Tabu Search":
            self.master.destroy()
            MenuTabuSearch()
        elif algorithm == "Genetic Algorithm":
            self.master.destroy()
            MenuGeneticAlgorithm()'''


class MenuBase(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        # exit to main menu button
        exit_button = tk.Button(self.master, text="Main Menu", command=self.exit_to_main_menu)
        exit_button.pack(side="bottom")

    def exit_to_main_menu(self):
        self.master.destroy()
        MainMenu().master.mainloop()
        

class MenuHillClimbing(MenuBase, tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Hill Climbing")
        self.title = tk.Label(self.master, text="Hill Climbing", font=("Arial", 12))
        self.title.pack(pady=10)
        
        self.question = tk.StringVar()
        self.question.set("Which type of neibourhoods do you want to use?")
        self.label_question = tk.Label(self.master, textvariable=self.question)
        self.label_question.pack()
        
        self.neighbourhood1 = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(self.master, text="Neighbourhood 1", variable=self.neighbourhood1)
        self.checkbox1.pack()
        self.neighbourhood2 = tk.IntVar()
        self.checkbox2 = tk.Checkbutton(self.master, text="Neighbourhood 2", variable=self.neighbourhood2)
        self.checkbox2.pack()
        self.neighbourhood3 = tk.IntVar()
        self.checkbox3 = tk.Checkbutton(self.master, text="Neighbourhood 3", variable=self.neighbourhood3)
        self.checkbox3.pack()
        
        self.run_button = tk.Button(self.master, text="Run", command=self.check_input)
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
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Menu Simulated Annealing")
        
        # cooling level
    
 
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