import random
import random_algorithm
import time_utils as tu
import tabu_search

# select parents --> roulette
def select_parents(solutions):
    min_time = min([solution[1] for solution in solutions])
    roullete = []
    total_val = 0
    for solution in solutions:
        roullete.append(min_time/solution[1])
        total_val += min_time/solution[1]
    roullete = [r/total_val for r in roullete]

    parents = []
    for _ in range(2):
        spin = random.random()
        for i, prob in enumerate(roullete):
            spin -= prob
            if spin <= 0:
                parents.append(solutions[i])
                break
    
    return parents



def est_arrival_time(graph, prev_arrival_time, prev_est, est):
    inspection_time = graph.nodes[prev_est]['inspectionDuration'] if prev_est != 0 else 0
    travel_time = tu.string_to_seconds(graph.edges[prev_est, est[0]]['travelTime'])
    arrival_time = tu.arrival_time(prev_arrival_time, prev_est, inspection_time, travel_time)
    return arrival_time

def remove_duplicates(graph, offspring, establishments):
    for van in offspring:
        van[:] = [est for est in van if est[0] not in establishments]
    
    for van in offspring:
        arrival_time = "09:00:00"
        prev_est = 0
        for est in van[1:]:
            est[:] = [est[0], est_arrival_time(graph, arrival_time, prev_est, est)]
            
    return offspring

def add_missing_establishments(graph, offspring, establishments):
    for est in establishments:
        # escolher van com menor arrival time
        chosen_van = min(offspring, key=lambda x: tu.string_to_seconds(x[-1][-1]))
        idx_van = offspring.index(chosen_van)
        offspring.pop(idx_van)
        
        # adicionar novo establishment
        chosen_van.pop()        
        at_new_est = est_arrival_time(graph, chosen_van[-1][-1], chosen_van[-1][0], est)
        chosen_van.append([est, at_new_est])
        final_at = est_arrival_time(graph, at_new_est, est, 0)
        chosen_van.append([0, final_at])
        
        offspring.append(chosen_van)
        
    return offspring   
    
    
# order-based crossover
def order_based_crossover(graph, parent1, parent2):
    # create crosspoints
    crosspoint1 = random.randint(0, len(parent1)-1)
    crosspoint2 = random.randint(0, len(parent1)-1)
    while crosspoint1 == crosspoint2:
        crosspoint2 = random.randint(1, len(parent1)-2)
    if crosspoint1 > crosspoint2:
        crosspoint1, crosspoint2 = crosspoint2, crosspoint1
        
    # pseudo create offspring 1
    begin_offs1 = parent1[:crosspoint1]
    subset_parent2 = parent2[crosspoint1:crosspoint2]
    end_offs1 = parent1[crosspoint2:]
    sub_offs1 = begin_offs1 + end_offs1
    
    # pseudo create offspring 2
    begin_offs2 = parent2[:crosspoint1]
    subset_parent1 = parent1[crosspoint1:crosspoint2]
    end_offs2 = parent2[crosspoint2:]
    sub_offs2 = begin_offs2 + end_offs2
    
    # remove duplicates
    visited_est1 = [est[0] for van in subset_parent2 for est in van if est[0] != 0]    
    sub_offs1 = remove_duplicates(graph, sub_offs1, visited_est1)
    
    visited_est2 = [est[0] for van in subset_parent1 for est in van if est[0] != 0]
    sub_offs1 = remove_duplicates(graph, sub_offs1, visited_est2)
   
    # add missing establishments
    offspring1 = sub_offs1 + subset_parent2
    offspring2 = sub_offs2 + subset_parent1
    to_visit1 = set(graph.nodes()) - set([est[0] for van in offspring1 for est in van])
    to_visit2 = set(graph.nodes()) - set([est[0] for van in offspring2 for est in van])
    
    offspring1 = add_missing_establishments(sub_offs1, to_visit1) + subset_parent2
    offspring2 = add_missing_establishments(sub_offs1, to_visit2) + subset_parent1

    return [offspring1, offspring2]
    



def genetic_algorithm(graph, n_vans, n_generations, mutation_prob):
    solutions = []
    # initialize population
    for _ in range(1000):
        solution = random_algorithm.calculate_random_paths(graph, "09.00.00", n_vans, 0)
        #fitness
        total_time = total_time(solution)
        solutions.append((solution, total_time))
    
    # select 100 best individuals according to fitness
    solutions = sorted(solutions, key=lambda x: x[1])
    solutions = solutions[:100]
    
    for _ in range(n_generations):
        # random.shuffle(solutions)
        
        # select parents
        parents = select_parents(solutions)
        parent1 = parents[0]
        parent2 = parents[1]
        
        # crossover
        offspring = order_based_crossover(graph, parent1, parent2)
        
        # mutation
        if (random.random() <= mutation_prob):
            offspring1 = tabu_search(offspring[0])
            offspring2 = tabu_search(offspring[1])
            offspring = [offspring1, offspring2]
        
        # discard dos 2 piores
        solutions.append(offspring)
        solutions = sorted(solutions, key=lambda x: x[1])
        solutions = solutions[:100]
    
    # terminate solution
    return solutions[0]