import time_utils
import random


def get_neighbourhood(graph, initialState):
    neighbourhood = []

    last_van = 0  # last van to finish
    max_time = 0

    for i, sublist in enumerate(initialState):
        for tup in sublist:
            if time_utils.string_to_seconds(tup[1]) > max_time:
                max_time = time_utils.string_to_seconds(tup[1])
                last_van = i

    # print(initialState)
    # print('\nlast van: ', last_van)

    # print('\n',initialState[last_van])

    for i in range(1, len(initialState[last_van]) - 2):
        for j in range(i + 1, len(initialState[last_van]) - 1):
            neighbour = initialState[last_van].copy()
            neighbour[i] = initialState[last_van][j]
            neighbour[j] = initialState[last_van][i]
            neighbourhood.append(
                initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour)] + initialState[
                                                                                             last_van + 1:])
            # print(time_utils.recalculate_hours(graph,neighbour))
            # print(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour)]+initialState[last_van+1:],'\n')

    # This for loop changes order os establishments in each van
    # for i in range(len(initialState)):
    #     for j in range(1,len(initialState[i])):
    #         #print(initialState[i])
    #         for k in range(j+1,len(initialState[i])-1):
    #             neighbour = initialState[i].copy()
    #             neighbour[j] = initialState[i][k]
    #             neighbour[k] = initialState[i][j]
    #             neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour)]+initialState[i+1:])
    # print(neighbourhood)

    # This for loop changes establishments between 2 vans
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
                    neighbourhood.append(
                        initialState[:i] + [time_utils.recalculate_hours(graph, neighbour2)] + initialState[
                                                                                               i + 1:last_van] + [
                            time_utils.recalculate_hours(graph, neighbour1)] + initialState[last_van + 1:])
                    # print(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:],'\n')
                    # print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
                    # print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))
                else:
                    neighbourhood.append(
                        initialState[:last_van] + [time_utils.recalculate_hours(graph, neighbour1)] + initialState[
                                                                                                      last_van + 1:i] + [
                            time_utils.recalculate_hours(graph, neighbour2)] + initialState[i + 1:])
                    # print(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:],'\n')
                    # print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
                    # print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))

    # This for loop changes establishments between 2 vans
    # for i in range(len(initialState)-1):
    #     for j in range(i+1,len(initialState)):
    #         for k in range(1,len(initialState[i])-1):
    #             for l in range(1,len(initialState[j])-1):

    #                 neighbour1 = initialState[i].copy()
    #                 neighbour2 = initialState[j].copy()
    #                 #if (j <= 1):
    #                     #print('\n\nn1: ',neighbour1)
    #                     #print('n2: ',neighbour2)

    #                 neighbour1[k] = initialState[j][l]
    #                 neighbour2[l] = initialState[i][k]
    #                 neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[i+1:j]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[j+1:])

    print(len(neighbourhood))

    return neighbourhood


def get_random_neighbour(graph, current_solution):
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

        establishment1_index = random.randint(1, len(current_solution[slowest_van]) - 1)
        # Keep generating the second random number until it's different from the first
        while True:
            establishment2_index = random.randint(1, len(current_solution[slowest_van]) - 1)
            if establishment1_index != establishment2_index:
                break

        # switch establishments
        temp = current_solution[slowest_van][establishment2_index]
        current_solution[slowest_van][establishment2_index] = current_solution[slowest_van][establishment1_index]
        current_solution[slowest_van][establishment1_index] = temp

    else: # switch establishment between slowest path and random path
        while True:
            random_van = random.randint(0, len(current_solution) - 1)
            if random_van != slowest_van:
                break

        if len(current_solution[random_van]) == 2:  # if random van didn't leave depot.
            establishment1_index = random.randint(1, len(current_solution[slowest_van]) - 1)
            # insert establishment between start and end
            current_solution[random_van].insert(1, current_solution[slowest_van][establishment1_index])
            # delete element added to random van from slowest van
            del current_solution[slowest_van][establishment1_index]

        else:
            establishment1_index = random.randint(1, len(current_solution[slowest_van]) - 1)
            establishment2_index = random.randint(1, len(current_solution[random_van]) - 1)

            temp = current_solution[random_van][establishment2_index]
            current_solution[random_van][establishment2_index] = current_solution[slowest_van][establishment1_index]
            current_solution[slowest_van][establishment1_index] = temp

    current_solution = time_utils.recalculate_hours(graph, current_solution)
    return current_solution
