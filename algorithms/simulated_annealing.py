import time
import utils
import time_utils
import random

def simulated_annealing(graph, solution, cooling_lever):
    best_solution = solution
    best_time = time_utils.total_time(best_solution)
    current_solution = solution
    current_time = time_utils.total_time(current_solution)

    initial_temperature = 100000
    temperature = initial_temperature
    final_temperature = 2000

    c = cooling_lever ** (-7) #! cooling_lever should be between 10 and 15, 10 ~= 100 secs; 15 (didn't test, around 30 minutes is my guess)

    iteration = 0
    while temperature > final_temperature:

        new_solution = utils.get_random_neighbour(graph, current_solution)
        new_time = time_utils.total_time(new_solution)

        if new_time < current_time:
            current_solution = new_solution
            current_time = new_time
            if new_time < best_time:
                best_solution = new_solution
                best_time = new_time
                print(best_time)
        else:
            #! acceptance prob starts at around 85%
            if utils.acceptance_probability(current_time, new_time, temperature) > random.randint(0, 100):
                current_solution = new_solution
                current_time = new_time

        temperature = initial_temperature /  (1 + c * iteration)
        iteration += iteration

    return best_solution