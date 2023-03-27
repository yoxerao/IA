import time_utils
import utils

def update_tabu_memory(tabu_memory):

    for i in range(len(tabu_memory)):
        for j in range(len(tabu_memory)):
            if(tabu_memory[i][j] != 0):
                tabu_memory[i][j] -= 1 

    return

def tabu_search(graph,initialState,numEstablishments):
    tabu_memory = [[0 for j in range(numEstablishments)] for i in range(numEstablishments)]

    interations = int(input('ENTER NUMBER OF INTERATION: '))
    
    while(interations != 0):

        last_van = 0  # last van to finish
        max_time = 0
        for j, sublist in enumerate(initialState):
            for tup in sublist:
                if time_utils.string_to_seconds(tup[1]) > max_time:
                    max_time = time_utils.string_to_seconds(tup[1])
                    last_van = j

        neighbourhood = utils.get_tabu_neighbourhood(graph,initialState,last_van,tabu_memory)
        best_neighbour = utils.get_best_neighbour(neighbourhood,initialState,last_van,tabu_memory)

        initialState = best_neighbour.copy()
        update_tabu_memory(tabu_memory)
        interations -= 1

    for i in range(numEstablishments):
        print(tabu_memory[i])


    print(time_utils.total_time(initialState))
    return
