import utils
import time_utils
import random

def simulated_annealing(graph, solution, max_time):
    best_solution = solution
    best_time = time_utils.total_time(best_solution)
    current_solution = solution
    current_time = time_utils.total_time(current_solution)
    temperature = 1
    cooling_rate = (0.0001/temperature) ** (1/max_time)
    while temperature > 0.0001:
        new_solution = utils.get_random_neighbour(graph, current_solution)
        new_time = time_utils.total_time(new_solution)
        if new_time < current_time:
            current_solution = new_solution
            current_time = new_time
            if new_time < best_time:
                best_solution = new_solution
                best_time = new_time
        else:
            if utils.acceptance_probability(current_time, new_time, temperature) > random.randint(0, 100):
                current_solution = new_solution
                current_time = new_time
        temperature *= cooling_rate
    return best_solution