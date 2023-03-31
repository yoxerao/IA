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

    iterations = int(input('ENTER NUMBER OF INTERATION: '))
    mutations_per_iteration = int(input('ENTER NUMBER OF MUTATIONS PER ITERATION: '))
    
    best_time = time_utils.string_to_seconds((time_utils.total_time(initialState))[1])
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

        neighbourhood = utils.get_tabu_neighbourhood(graph,initialState,last_van,tabu_memory,mutations_per_iteration)
        #print('hello')
        best_neighbour = utils.get_best_neighbour(neighbourhood,initialState,last_van,tabu_memory,mutations_per_iteration)
        #print('hello2')
        initialState = best_neighbour.copy()

        new_time = time_utils.string_to_seconds((time_utils.total_time(initialState))[1])

        if (new_time < best_time):
            best_time = new_time
            counter = 150
        else:
            counter -= 1

        update_tabu_memory(tabu_memory)
        iterations -= 1
        print(iterations)
        print(time_utils.total_time(initialState))
        #print(best_time)


    #for i in range(numEstablishments):
        #print(tabu_memory[i])


    print(time_utils.total_time(initialState))
    print(time_utils.seconds_to_string(best_time))
    print(iterations)
    return 
