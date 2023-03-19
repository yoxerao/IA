import random
import random_algorithm


# swap mutation
def s_mutation(parent1, parent2):


# order-based crossover
def ob_crossover(parent1, parent2, n_establishments):
    sub_size = random.randint(1, len(parent1)-1)
    sub_indices = random.sample(range(len(parent1)), sub_size)
    sub_parent1 = [parent1[i] for i in sub_indices]
    sub_establishments = [est[0] for van1 in sub_parent1 for est in van1] # list of the establishments that are already in the offspring
    
    for van2 in parent2: # para cada carrinha
        new_establishments = [est[0] for est in van2 if est[0] not in sub_establishments] # list of establishments not in the offspring
        if len(new_establishments) == 0:
            continue;
        for i, van1 in enumerate(sub_parent1):
            if(n_establishments-len(sub_establishments)-len(new_establishments) == 0):
                continue
            
            
            
        
    return offspring1




def genetic_algorithm(graph, n_vans, n_establishments, n_generations, crossover_prob):
    solutions = []
    for _ in range(1000):
        solution = random_algorithm.calculate_random_paths(graph, "09:00:00", n_vans, 1) # initialize population
        total_time = total_time(solution) #fitness
        solutions.append((solution, total_time))
    sorted_solutions = sorted(solutions, key=lambda x: x[1])
    best_solutions = sorted_solutions[:2]
    for _ in range(n_generations):
        # select parents
        parent1 = best_solutions[0][0]
        parent2 = best_solutions[1][0]
        if (random.random() <= crossover_prob):
            offspring1, offspring2 = ob_crossover(parent1, parent2, n_establishments)
        else:
            offspring1, offspring2 = s_mutation(parent1, parent2)
        best_solutions.append(offspring1)
        best_solutions.append(offspring2)
        best_solutions = sorted(solutions, key=lambda x: x[1])
        best_solutions = best_solutions[:2]