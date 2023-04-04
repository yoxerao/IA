import time
import neighbours
import time_utils
import random
import math
import copy
import networkx as nx
from time import sleep

#? Calculates probability of accepting a worse solution based on the temperature and the difference in time
def acceptance_probability(current_time, new_time, temperature):
    delta = new_time - current_time
    scaling_factor = 10000.0 / (delta + 1000.0)
    if delta <= 0:
        return 100
    else:
        if(100*math.exp(-delta/(temperature*scaling_factor)) > 5):
            print("delta: " + str(delta))
            print("prob: " + str(100*math.exp(-delta/(temperature*scaling_factor))))
        return 100 * math.exp(-delta / (temperature * scaling_factor))


def simulated_annealing(graph, solution, cooling_lever):
    best_solution = solution
    best_time = time_utils.string_to_seconds(time_utils.total_time(best_solution))
    current_solution = solution
    current_time = time_utils.string_to_seconds(time_utils.total_time(current_solution))

    initial_temperature = 1000
    temperature = initial_temperature
    final_temperature = 5

    #! cooling_lever (input) should be between 5 and 7 for best results
    cooling_factor = cooling_lever ** (-3)

    iteration = 0
    while temperature > final_temperature:
        
        new_solution = neighbours.get_random_neighbour(graph, current_solution)
        new_time = time_utils.string_to_seconds(time_utils.total_time(new_solution))

        if new_time < current_time:
            current_solution = new_solution
            current_time = new_time

            if new_time < best_time:
                best_solution = new_solution
                best_time = new_time
                print("NEW BEST:" + time_utils.seconds_to_string(best_time))
        else:
            #? Accept worse solution with probability based on temperature and difference in time
            if acceptance_probability(current_time, new_time, temperature) > random.randint(0, 100):
                current_solution = new_solution
                current_time = new_time


        if iteration % 1000 == 0:
            print("temperature: " + str(temperature))

        #? decrease temperature
        temperature = initial_temperature / (1 + cooling_factor * iteration)

        iteration += 1

    print("FINAL SOLUTION: " + time_utils.seconds_to_string(best_time) + "\n" + str(best_solution))
    return best_solution
