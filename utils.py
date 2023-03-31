import time_utils
import random
import math
import time
import copy


def get_best_neighbour(neighbourhood,initialState,last_van,tabu_memory,number_of_checks):
    best_neighbour_index = -1
    establishments_changed = [0,0]
    counter = number_of_checks


    for i in range(len(neighbourhood)):
    # while((len(neighbourhood) != 0) and (counter != 0)):
    #     random_neighbour = random.randint(0,len(neighbourhood)-1)
    #     print(len(neighbourhood))


        for j in range(len(initialState[last_van])):
            establishment1 = initialState[last_van][j][0]
            establishment2 = neighbourhood[i][last_van][j][0]
            # If condition to check what establishments were changed
            if( establishment1 != establishment2):
                # If there is no tenure for this change we consider it as the new best neighbour
                if(tabu_memory[establishment1][establishment2] == 0):
                    new_neighbour = time_utils.string_to_seconds(time_utils.total_time(neighbourhood[i])[1])
                    if(best_neighbour_index == -1):
                        best_neighbour = new_neighbour + 1 
                    else:
                        best_neighbour = time_utils.string_to_seconds(time_utils.total_time(neighbourhood[best_neighbour_index])[1])

                    if(new_neighbour < best_neighbour):
                        #print('\n',new_neighbour)
                        #print(best_neighbour)
                        best_neighbour_index = i
                        establishments_changed[0] = initialState[last_van][j][0]
                        establishments_changed[1] = neighbourhood[i][last_van][j][0]
        #neighbourhood.remove(neighbourhood[random_neighbour])                  
        counter -= 1

    #print(establishments_changed)

    # Update tabu memory with tenure
    if(establishments_changed[0] != 0):
        tabu_memory[establishments_changed[0]][establishments_changed[1]] = 5
        tabu_memory[establishments_changed[1]][establishments_changed[0]] = 5

    if(best_neighbour_index == -1):
        return []
    else:
        #print(neighbourhood[best_neighbour_index])
        return neighbourhood[best_neighbour_index]

def get_tabu_neighbourhood(graph,initialState,last_van,tabu_memory,mutations_per_iteration):
    neighbourhood = []
    already_changed = [] # A list to check if a specific swap as already been made [random_van,random_establishment_from_van,random_establishment_from_last_van]

    counter = 0

    for i in range(1, len(initialState[last_van]) - 2):
        for j in range(i + 1, len(initialState[last_van]) - 1):
            if(tabu_memory[i][j] != 0):
                continue

            neighbour = initialState[last_van].copy()
            neighbour[i] = initialState[last_van][j]
            neighbour[j] = initialState[last_van][i]

            new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour)] + initialState[last_van + 1:]
            neighbourhood.append(new_neighbour)


    #print(len(neighbourhood))

    while(counter != mutations_per_iteration):

        random_van = random.randint(0,len(initialState)-1) #Generating a random van to swap with the last one
        
        
        while(random_van == last_van):   #while loop in case the selected van was the same as the last one
            random_van = random.randint(0,len(initialState)-1)
        
        random_establishment = random.randint(1,len(initialState[random_van])-2)  #random establishment from random van
        random_establishment2 = random.randint(1,len(initialState[last_van])-2)   #random establishment from last van

        random_values = [random_van,random_establishment,random_establishment2]

        if(random_values not in already_changed):
            already_changed.append(random_values)
        else:
            #print(already_changed)
            #print('found one')
            continue


        if(tabu_memory[random_van][random_establishment] != 0):
            continue

        neighbour1 = initialState[last_van].copy()
        neighbour2 = initialState[random_van].copy()
        # print('\n\nn1: ',neighbour1)
        # print('n2: ',neighbour2)
        neighbour1[random_establishment2] = initialState[random_van][random_establishment]
        neighbour2[random_establishment] = initialState[last_van][random_establishment2]
        # print('\nnew n1: ',neighbour1)
        # print('new n2: ',neighbour2)

        if(random_van < last_van):
            new_neighbour = initialState[:random_van] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[random_van + 1:last_van] + [time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:]
            neighbourhood.append(new_neighbour)

        else:
            new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:random_van] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[random_van + 1:]
            neighbourhood.append(new_neighbour)

        counter += 1



    # for i in range(len(initialState)):
    #     if (i == last_van):
    #         continue
    #     for j in range(1, len(initialState[last_van]) - 1):
    #         for k in range(1, len(initialState[i]) - 1):

    #             if(tabu_memory[j][k] != 0):
    #                 continue

    #             neighbour1 = initialState[last_van].copy()
    #             neighbour2 = initialState[i].copy()
    #             # print('\n\nn1: ',neighbour1)
    #             # print('n2: ',neighbour2)
    #             neighbour1[j] = initialState[i][k]
    #             neighbour2[k] = initialState[last_van][j]
    #             # print('\nnew n1: ',neighbour1)
    #             # print('new n2: ',neighbour2)


    #             if (i < last_van):

    #                 new_neighbour = initialState[:i] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[i + 1:last_van] + [time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:]
    #                 neighbourhood.append(new_neighbour)

    #                 # print(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:],'\n')
    #                 # print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
    #                 # print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))
    #             else:
    #                 new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:i] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[i + 1:]
    #                 neighbourhood.append(new_neighbour)
    #                 # print(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:],'\n')
    #                 # print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
    #                 # print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))

    #print(len(neighbourhood))
    return neighbourhood


def swap_establishments_in_van(graph,initialState,last_van):
    for i in range(1, len(initialState[last_van]) - 2):
        for j in range(i + 1, len(initialState[last_van]) - 1):
            neighbour = initialState[last_van].copy()
            neighbour[i] = initialState[last_van][j]
            neighbour[j] = initialState[last_van][i]

            new_neighbour = initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour)] + initialState[
                                                                                                         last_van + 1:]
            # print(new_neighbour)
            if (time_utils.string_to_seconds(time_utils.total_time(new_neighbour)[1]) < time_utils.string_to_seconds(
                    time_utils.total_time(initialState)[1])):
                return new_neighbour

    return []


def swap_establishments_between_van(graph, initialState, last_van):
    for i in range(len(initialState)):
        if (i == last_van):
            continue
        for j in range(1, len(initialState[last_van]) - 1):
            for k in range(1, len(initialState[i]) - 1):
                neighbour1 = initialState[last_van].copy()
                neighbour2 = initialState[i].copy()
                # print('\n\nn1: ',neighbour1)
                # print('n2: ',neighbour2)
                neighbour1[j] = initialState[i][k]
                neighbour2[k] = initialState[last_van][j]
                # print('\nnew n1: ',neighbour1)
                # print('new n2: ',neighbour2)

                if (i < last_van):

                    new_neighbour = initialState[:i] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[
                                                                                                           i + 1:last_van] + [
                                        time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:]
                    if (time_utils.string_to_seconds(
                            time_utils.total_time(new_neighbour)[1]) < time_utils.string_to_seconds(
                            time_utils.total_time(initialState)[1])):
                        return new_neighbour

                    # print(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:],'\n')
                    # print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
                    # print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))
                else:
                    new_neighbour = initialState[:last_van] + [
                        time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:i] + [
                                        time_utils.recalculate_hours(graph, neighbour2)] + initialState[i + 1:]
                    if (time_utils.string_to_seconds(
                            time_utils.total_time(new_neighbour)[1]) < time_utils.string_to_seconds(
                            time_utils.total_time(initialState)[1])):
                        return new_neighbour
                    # print(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:],'\n')
                    # print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
                    # print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))
    return []


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

    print(len(neighbourhood))

    return neighbourhood


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


def acceptance_probability(current_time, new_time, temperature):
    delta = new_time - current_time
    if delta <= 0:
        return 100
    else:
        #print("ct:" + current_time + "nt:" + new_time)
        #print(100 * math.exp(-delta / temperature))
        return 100 * math.exp(-delta / temperature)
