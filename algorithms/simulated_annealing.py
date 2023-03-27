import time
import utils
import time_utils
import random


def simulated_annealing(graph, solution, cooling_lever):
    best_solution = solution
    best_time = time_utils.string_to_seconds(time_utils.total_time(best_solution)[1])
    current_solution = solution
    current_time = time_utils.string_to_seconds(time_utils.total_time(current_solution)[1])

    initial_temperature = 100000
    temperature = initial_temperature
    final_temperature = 2000
    # ! cooling_lever should be between 5 and 7
    c = cooling_lever ** (-5)

    iteration = 0
    while temperature > final_temperature:

        new_solution = utils.get_random_neighbour(graph, current_solution)
        new_time = time_utils.string_to_seconds(time_utils.total_time(new_solution)[1])

        if new_time < current_time:
            current_solution = new_solution
            current_time = new_time

            if new_time < best_time:
                best_solution = new_solution
                best_time = new_time
                print("NEW BEST:" + time_utils.seconds_to_string(best_time) + " " + str(best_solution))
        else:

            if utils.acceptance_probability(current_time, new_time, temperature) > random.randint(0, 100):
                current_solution = new_solution
                current_time = new_time


        if iteration % 1000 == 0:
            print("temperature: " + str(temperature))

        #print(temperature)
        temperature = initial_temperature / (1 + c * iteration)
        iteration += 1

    return best_solution
