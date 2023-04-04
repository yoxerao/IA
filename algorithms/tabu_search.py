import time_utils
import neighbours

def update_tabu_memory(tabu_memory):
    for i in range(len(tabu_memory)):
        for j in range(len(tabu_memory)):
            if(tabu_memory[i][j] != 0):
                tabu_memory[i][j] -= 1 
    return

def tabu_search(graph,initialState,numEstablishments, iterations, mutations_per_iteration):
    tabu_memory = [[0 for j in range(numEstablishments)] for i in range(numEstablishments)]


    best_time = time_utils.string_to_seconds((time_utils.total_time(initialState)))
    counter = 150

    #print(best_time)

    while((iterations != 0) and (counter != 0)):
        last_van = 0  # last van to finish
        max_time = 0
        for j, sublist in enumerate(initialState):
            for tup in sublist:
                if time_utils.string_to_seconds(tup[1]) > max_time:
                    max_time = time_utils.string_to_seconds(tup[1])
                    last_van = j

        neighbourhood = neighbours.get_tabu_neighbourhood(graph,initialState,last_van,tabu_memory,mutations_per_iteration)
        best_neighbour = neighbours.get_best_neighbour(neighbourhood,initialState,last_van,tabu_memory,mutations_per_iteration)
        initialState = best_neighbour.copy()

        new_time = time_utils.string_to_seconds((time_utils.total_time(initialState)))

        if (new_time < best_time):
            best_time = new_time
            counter = 150
        else:
            counter -= 1

        update_tabu_memory(tabu_memory)
        iterations -= 1


    #for i in range(numEstablishments):
        #print(tabu_memory[i])


   

    return initialState
