import time_utils
import random
import copy

# tries to find a better solution than initialState by swapping establishments within a single van
def swap_establishments_in_van(graph, initialState, last_van):
    # generates all possible pairs of establishments that can be swapped
    for i in range(1, len(initialState[last_van]) - 2):
        for j in range(i + 1, len(initialState[last_van]) - 1):
            # create a new neighbour (by swapping the establishments at indices i and j)
            neighbour = initialState[last_van].copy()
            neighbour[i] = initialState[last_van][j]
            neighbour[j] = initialState[last_van][i]
            
            # create a new list by replacing the last_van with the modified neighbour
            new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour)] + initialState[
                                                                                                         last_van + 1:]
            
            # in case the total time taken by the new neighbour is less than the total time taken by the current state --> return new neighbour 
            if (time_utils.string_to_seconds(time_utils.total_time(new_neighbour)) < time_utils.string_to_seconds(
                    time_utils.total_time(initialState))):
                return new_neighbour

    return []

# tries to find a better solution than initialState by swapping establishments between two different vans
def swap_establishments_between_van(graph, initialState, last_van):
    # loop over all vans in initialState
    for i in range(len(initialState)):
        # skip the last van, since we only want to swap establishments between different vans
        if (i == last_van):
            continue
        # loop over establishments in last van
        for j in range(1, len(initialState[last_van]) - 1):
            # loop over establishments in the other van
            for k in range(1, len(initialState[i]) - 1):
                neighbour1 = initialState[last_van].copy()
                neighbour2 = initialState[i].copy()
                # swap the two establishments between the two sublists
                neighbour1[j] = initialState[i][k]
                neighbour2[k] = initialState[last_van][j]
                
                # check if the new solution is better than the initial solution
                if (i < last_van):
                    # if the other van comes before the last van, update the sublists accordingly
                    new_neighbour = initialState[:i] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[
                                                                                                           i + 1:last_van] + [
                                        time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:]
                    # check if the new solution is better than the initial solution and if so, return it
                    if (time_utils.string_to_seconds(
                            time_utils.total_time(new_neighbour)) < time_utils.string_to_seconds(
                        time_utils.total_time(initialState))):
                        return new_neighbour

                else:
                    # if the other van comes after the last van, update the sublists accordingly
                    new_neighbour = initialState[:last_van] + [
                        time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:i] + [
                                        time_utils.recalculate_hours(graph, neighbour2)] + initialState[i + 1:]
                    if (time_utils.string_to_seconds(
                            time_utils.total_time(new_neighbour)) < time_utils.string_to_seconds(
                        time_utils.total_time(initialState))):
                        return new_neighbour
    return []



# finds the best neighbour solution from a given neighbourhood, considering a tabu memory that keeps track of previously explored solutions
def get_best_neighbour(neighbourhood, initialState, last_van, tabu_memory, number_of_checks):
    best_neighbour_index = -1
    establishments_changed = [0, 0]
    counter = number_of_checks
    
    # loop through all neighbours in the neighbourhood
    for i in range(len(neighbourhood)):
        # loop through all establishments in the current van
        for j in range(len(initialState[last_van])):
            establishment1 = initialState[last_van][j][0] # current establishment
            establishment2 = neighbourhood[i][last_van][j][0] # establishment in current neighbour
            # If condition to check what establishments were changed
            if (establishment1 != establishment2):
                # If there is no tenure for this change we consider it as the new best neighbour
                if (tabu_memory[establishment1][establishment2] == 0):
                    new_neighbour = time_utils.string_to_seconds(time_utils.total_time(neighbourhood[i]))
                    # check if the current neighbour is better than the best neighbour found so far
                    if (best_neighbour_index == -1):
                        best_neighbour = new_neighbour + 1
                    else:
                        best_neighbour = time_utils.string_to_seconds(
                            time_utils.total_time(neighbourhood[best_neighbour_index]))

                    if (new_neighbour < best_neighbour):
                        # if current neighbour is better, update best neighbour
                        best_neighbour_index = i
                        establishments_changed[0] = initialState[last_van][j][0]
                        establishments_changed[1] = neighbourhood[i][last_van][j][0]
        counter -= 1

    # Update tabu memory with tenure
    if (establishments_changed[0] != 0):
        tabu_memory[establishments_changed[0]][establishments_changed[1]] = 5
        tabu_memory[establishments_changed[1]][establishments_changed[0]] = 5
        
    # return the best neighbour found
    if (best_neighbour_index == -1):
        return []
    else:
        return neighbourhood[best_neighbour_index]


# generates a neighbourhood of solutions by performing swaps of establishments between two randomly chosen vans, while keeping track of already made swaps and using a tabu memory to prevent returning to previously explored solutions
def get_tabu_neighbourhood(graph, initialState, last_van, tabu_memory, mutations_per_iteration):
    neighbourhood = [] # A list to store the generated neighbourhood
    already_changed = []  # A list to check if a specific swap as already been made [random_van,random_establishment_from_van,random_establishment_from_last_van]

    counter = 0

    # the swaps inside a van are few compared to the ones made between vans so we generate 
    # all swaps inside a van and they don't count for the mutations_per_iterations variable
    for i in range(1, len(initialState[last_van]) - 2):
        for j in range(i + 1, len(initialState[last_van]) - 1):
            if (tabu_memory[i][j] != 0):
                continue

            neighbour = initialState[last_van].copy()
            neighbour[i] = initialState[last_van][j]
            neighbour[j] = initialState[last_van][i]

            new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour)] + initialState[
                                                                                                         last_van + 1:]
            neighbourhood.append(new_neighbour)

    # generate swaps between the last_van and a random van, and add them to the neighbourhood
    while (counter != mutations_per_iteration):

        random_van = random.randint(0, len(initialState) - 1)  # Generating a random van to swap with the last one

        while (random_van == last_van):  # while loop in case the selected van was the same as the last one
            random_van = random.randint(0, len(initialState) - 1)

        if(len(initialState[random_van]) == 2):
            random_establishment == -1 # if the random van is empty, we simply add random establishment from the last van
            random_establishment2 = random.randint(1, len(initialState[last_van]) - 2)  # random establishment from last van
        else: 
            random_establishment = random.randint(1, len(initialState[random_van]) - 2)  # random establishment from random van
            random_establishment2 = random.randint(1, len(initialState[last_van]) - 2)  # random establishment from last van

        random_values = [random_van, random_establishment, random_establishment2]
        
        # if the selected swap has already been made, skip it and generate a new one
        if (random_values not in already_changed):
            already_changed.append(random_values)
        else:
            continue
        
        # if the selected swap is tabu, skip it and generate a new one
        if (tabu_memory[random_van][random_establishment] != 0):
            continue
        
        # perform the swap between the two vans
        neighbour1 = initialState[last_van].copy()
        neighbour2 = initialState[random_van].copy()
        if (random_establishment == -1):
            neighbour2.insert(1,initialState[last_van][random_establishment2])
            del neighbour1[random_establishment2]
        else:
            neighbour1[random_establishment2] = initialState[random_van][random_establishment]
            neighbour2[random_establishment] = initialState[last_van][random_establishment2]
        
        # generate a new state based on the new neighbourhood
        if (random_van < last_van):
            new_neighbour = initialState[:random_van] + [
                time_utils.recalculate_hours(graph, neighbour2)] + initialState[random_van + 1:last_van] + [
                                time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:]
            neighbourhood.append(new_neighbour)

        else:
            new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour1)] + initialState[
                                                                                                          last_van + 1:random_van] + [
                                time_utils.recalculate_hours(graph, neighbour2)] + initialState[random_van + 1:]
            neighbourhood.append(new_neighbour)

        counter += 1

    return neighbourhood


# generates a neighborhood of solutions by swapping establishments within the last van to finish and between the last van and a randomly selected van
def get_neighbourhood(graph, initialState):
    neighbourhood = []

    last_van = 0  # last van to finish
    max_time = 0

    for i, sublist in enumerate(initialState):
        for tup in sublist:
            if time_utils.string_to_seconds(tup[1]) > max_time:
                max_time = time_utils.string_to_seconds(tup[1])
                last_van = i

    swap_establishments_in_van(graph, initialState, last_van, neighbourhood)
    swap_establishments_between_van(graph, initialState, last_van, neighbourhood)

    return neighbourhood


# generates a random neighboring solution from the given solution by swapping establishments within or between vans
def get_random_neighbour(graph, real_current_solution):
    current_solution = copy.deepcopy(real_current_solution)
    slowest_van = 0  # last van to finish
    max_time = 0

    # find the slowest van
    for i, sublist in enumerate(current_solution):
        for tup in sublist:
            if time_utils.string_to_seconds(tup[1]) > max_time:
                max_time = time_utils.string_to_seconds(tup[1])
                slowest_van = i

    coin = random.randint(0, 1)
    if len(current_solution) == 1:  # if there's only one van we cant do the second option
        coin = 0

    if coin == 0:  # switch between 2 establishments in slowest path

        establishment1_index = random.randint(1, len(current_solution[slowest_van]) - 2)
        # Keep generating the second random number until it's different from the first
        while True:
            establishment2_index = random.randint(1, len(current_solution[slowest_van]) - 2)
            if establishment1_index != establishment2_index:
                break

        # switch establishments
        temp = current_solution[slowest_van][establishment2_index]
        current_solution[slowest_van][establishment2_index] = current_solution[slowest_van][establishment1_index]
        current_solution[slowest_van][establishment1_index] = temp

    else:  # switch establishment between slowest path and random path
        while True:
            random_van = random.randint(0, len(current_solution) - 1)
            if random_van != slowest_van:
                break

        if len(current_solution[random_van]) == 2:  # if random van didn't leave depot.
            establishment1_index = random.randint(1, len(current_solution[slowest_van]) - 2)
            # insert establishment between start and end
            current_solution[random_van].insert(1, current_solution[slowest_van][establishment1_index])
            # delete element added to random van from slowest van
            del current_solution[slowest_van][establishment1_index]

        else:
            establishment1_index = random.randint(1, len(current_solution[slowest_van]) - 2)
            establishment2_index = random.randint(1, len(current_solution[random_van]) - 2)

            temp = current_solution[random_van][establishment2_index]
            current_solution[random_van][establishment2_index] = current_solution[slowest_van][establishment1_index]
            current_solution[slowest_van][establishment1_index] = temp
        time_utils.recalculate_hours(graph, current_solution[random_van])

    time_utils.recalculate_hours(graph, current_solution[slowest_van])

    return current_solution

