import random
import time_utils as tu
from algorithms.random_algorithm import calculate_random_paths
from algorithms.tabu_search import tabu_search
import copy

# select parents --> roulette
def select_parents(solutions):
    min_time = min([solution[1] for solution in solutions]) # get the lower value (the fittest)
    roullete = []
    total_val = 0
    for solution in solutions:
        roullete.append(tu.string_to_seconds(min_time)/tu.string_to_seconds(solution[1]))
        total_val += tu.string_to_seconds(min_time)/tu.string_to_seconds(solution[1])
    roullete = [r/total_val for r in roullete] # normalize the values: between 0 and 1; the bigger the fittest (the lower total time)
    parents = []
    for _ in range(2):
        spin = random.random()
        for i, prob in enumerate(roullete):
            spin -= prob
            if spin <= 0:
                parents.append(solutions[i][0])
                break
    return parents


# calcuçate arrival time at a establishment knowing the previous visited establishment
def est_arrival_time(graph, prev_arrival_time, prev_est, est):
    inspection_time = graph.nodes[prev_est]['inspectionDuration'] if prev_est != 0 else 0
    travel_time = tu.string_to_seconds(graph.edges[prev_est, est]['travelTime'])
    arrival_time = tu.arrival_time(prev_arrival_time, graph.nodes[prev_est], inspection_time, travel_time) 
    return arrival_time

def remove_duplicates(graph, offspring, establishments):
    for van in offspring:
        van[:] = (est for est in van if est[0] not in establishments) # only keep the 'new' establishments 
    
    # update arrival times
    for van in offspring:
        arrival_time = "09.00.00"
        prev_est = 0
        if(len(van) == 2): # in case there are no establishments to visit (only the depot)
            van = [van[0], van[0]]
        else:
            for i, est in enumerate(van[1:]):
                this_arrival_time = est_arrival_time(graph, arrival_time, prev_est, est[0])
                est = (est[0], this_arrival_time)
                prev_est = est[0]
                arrival_time = this_arrival_time
                van[i+1] = est
          
    return offspring


def add_missing_establishments(graph, offspring, establishments):
    for est in establishments:
        # chose van with the lowest arrival time
        chosen_van = min(offspring, key=lambda x: tu.string_to_seconds(x[-1][-1]))
        idx_van = offspring.index(chosen_van)
        offspring.pop(idx_van)
        
        # add a new establishment (of the list of esyablishment still to visit)
        chosen_van.pop() # take the depot of the end of the list
        at_new_est = est_arrival_time(graph, chosen_van[-1][1], chosen_van[-1][0], est)
        chosen_van.append((est, at_new_est))
        final_at = est_arrival_time(graph, at_new_est, est, 0)
        chosen_van.append((0, final_at))
        offspring.append(chosen_van)

    return offspring   
    
    
# crossover --> order-based 
def order_based_crossover(graph, parent1, parent2):
    # create crosspoints
    crosspoint1 = random.randint(1, len(parent1)-1)
    crosspoint2 = random.randint(1, len(parent1)-1)
    while crosspoint1 == crosspoint2:
        crosspoint2 = random.randint(1, len(parent1)-1)
    if crosspoint1 > crosspoint2:
        crosspoint1, crosspoint2 = crosspoint2, crosspoint1
    
    # create starting elements of offspring 1: beginning of parent1, middle of parent2, ending of parent1
    begin_offs1 = parent1[:crosspoint1]
    middle_parent2_ = parent2[crosspoint1:crosspoint2]
    end_offs1 = parent1[crosspoint2:]
    sub_offs1_ = begin_offs1 + end_offs1
    middle_parent2 = copy.deepcopy(middle_parent2_)
    sub_offs1 = copy.deepcopy(sub_offs1_)
    
    # create starting elements of offspring 2: beginning of parent2, middle of parent1, ending of parent2
    begin_offs2 = parent2[:crosspoint1]
    middle_parent1_ = parent1[crosspoint1:crosspoint2]
    end_offs2 = parent2[crosspoint2:]
    sub_offs2_ = begin_offs2 + end_offs2
    middle_parent1 = copy.deepcopy(middle_parent1_)
    sub_offs2 = copy.deepcopy(sub_offs2_)
    
    # remove duplicates (from begin and end subsets)
    visited_est1 = [est[0] for van in middle_parent2 for est in van if est[0] != 0] # check which establishment are already visited
    sub_offs1 = remove_duplicates(graph, sub_offs1, visited_est1)
    visited_est2 = [est[0] for van in middle_parent1 for est in van if est[0] != 0]
    sub_offs2 = remove_duplicates(graph, sub_offs2, visited_est2)
    
    # add missing establishments
    offspring1 = sub_offs1 + middle_parent2
    offspring2 = sub_offs2 + middle_parent1
    to_visit1 = set(graph.nodes()) - set([est[0] for van in offspring1 for est in van]) # check which establishments are there still to visit
    to_visit2 = set(graph.nodes()) - set([est[0] for van in offspring2 for est in van])
    
    sub_offs1 = add_missing_establishments(graph, sub_offs1, to_visit1)
    offspring1 = sub_offs1 + middle_parent2
    sub_offs2 = add_missing_establishments(graph, sub_offs2, to_visit2)
    offspring2 = sub_offs2 + middle_parent1

    return offspring1, offspring2
    

# mutation --> swap (random)
def swap_mutation(graph,offspring):
    van1_index = random.randint(0, len(offspring)-1)
    van2_index = random.randint(0, len(offspring)-1)
    while van1_index == van2_index:
            van2_index = random.randint(0, len(offspring)-1)
    
    van1 = offspring[van1_index]
    van2 = offspring[van2_index]
    print(van1_index)
    print(van2_index)
        
    # in case the van 1 doesn't have any establishments --> add one random establishment from van 2
    if(len(van1) == 2 and len(van2) > 2):
        est_van2_index = random.randint(1, len(van2)-2)
        est_van2 = van2[est_van2_index]
        van1 = van1[0] + est_van2 + van1[1]
        van2.pop(est_van2_index)
    
    # in case the van 2 doesn't have any establishments --> add one random establishment from van 1
    elif (len(van2) == 2 and len(van1) > 2):
        est_van1_index = random.randint(1, len(van1)-2)
        est_van1 = van1[est_van1_index]
        van2 = van2[0] + est_van1 + van2[1]
        van1.pop(est_van1_index)
    
    # in case neither of the vans have establishments
    elif (len(van1) == len(van2) == 2):
        return offspring
    
    else:
        max_est_index = min(len(van1), len(van2))

        est_van1_index = random.randint(1, max_est_index-2)
        est_van2_index = random.randint(1, max_est_index-2)
        est_van1 = van1[est_van1_index]
        est_van2 = van2[est_van2_index]
        
        van1[est_van1_index] = est_van2 
        van2[est_van2_index] = est_van1
    print(est_van1_index)
    print(est_van2_index)
    # update arrival times on mutated vans
    for van in (van1, van2):
        arrival_time = "09.00.00"
        prev_est = 0
        if(len(van) == 2): # in case there are no establishments to visit (only the depot)
            van = [van[0], van[0]]
            print("OLA")
        else:
            for i, est in enumerate(van[1:]):
                this_arrival_time = est_arrival_time(graph, arrival_time, prev_est, est[0])
                est = (est[0], this_arrival_time)
                prev_est = est[0]
                arrival_time = this_arrival_time
                van[i+1] = est
    
    return offspring


        
def genetic_algorithm(graph, n_vans, n_establishments, n_generations, mutation_prob, mutation_type):
    solutions = []
    
    # initialize population
    for _ in range(100):
        solution = calculate_random_paths(graph, "09.00.00", n_vans, 0)
        #fitness
        total_time = tu.total_time(solution)
        solutions.append((solution, total_time))
    
    # select 50 best individuals according to fitness
    solutions = sorted(solutions, key=lambda x: tu.string_to_seconds(x[1]))
    solutions = solutions[:50]
    
    first_parent = []
    second_parent = []
    
    for i in range(n_generations):
        print('generation number ', i)
        
        # select parents --> roullete
        parents = select_parents(solutions)
        parent1 = parents[0]
        parent2 = parents[1]
        if i == 0:
            first_parent = parent1
            second_parent = parent2
            
        # crossover --> order-based
        offspring1, offspring2 = order_based_crossover(graph, parent1, parent2)
        
        # mutation --> tabu search
        if (random.random() <= mutation_prob):
            print(' -> mutation!')
            if(mutation_type == 0):
                offspring1 = swap_mutation(graph, offspring1)
                offspring2 = swap_mutation(graph, offspring2)
            if(mutation_type == 1):
                print('    offspring 1')
                offspring1 = tabu_search(graph,offspring1,n_establishments, 1000, 150)
                print('    offspring 2')
                offspring2 = tabu_search(graph,offspring2,n_establishments, 1000, 150)
        
        total_time1 = tu.total_time(offspring1)
        total_time2 = tu.total_time(offspring2)
        offspring = [(offspring1, total_time1), (offspring2, total_time2)]
        
        # discard two least fit individuals
        new_solutions = solutions + offspring
        new_solutions = sorted(new_solutions, key=lambda x: tu.string_to_seconds(x[1]))
        solutions = new_solutions[:50]


    return solutions[0][0], first_parent, second_parent