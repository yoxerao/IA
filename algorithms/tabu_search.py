import time_utils
import neighbours

# function to update the tabu memory
def update_tabu_memory(tabu_memory):
    for i in range(len(tabu_memory)):
        for j in range(len(tabu_memory)):
            if(tabu_memory[i][j] != 0):
                tabu_memory[i][j] -= 1 
    return

def tabu_search(graph,initialState,numEstablishments, iterations, mutations_per_iteration):
    # initialize tabu memory with all zeros

    tabu_memory = [[0 for j in range(numEstablishments)] for i in range(numEstablishments)]

    # initialize the best time to the total time of the initial state
    best_time = time_utils.string_to_seconds((time_utils.total_time(initialState)))
    # set a counter to control when to exit the loop
    counter = 150
    
    # run the loop until either the desired number of iterations is reached or the counter reaches 0
    while((iterations != 0) and (counter != 0)):
        last_van = 0  # last van to finish
        max_time = 0 # respective time taken
        for j, sublist in enumerate(initialState):
            for tup in sublist:
                if time_utils.string_to_seconds(tup[1]) > max_time:
                    max_time = time_utils.string_to_seconds(tup[1])
                    last_van = j
                    
        # get the neighbourhood using the tabu search strategy
        neighbourhood = neighbours.get_tabu_neighbourhood(graph,initialState,last_van,tabu_memory,mutations_per_iteration, numEstablishments)
        # get the best neighbour from the neighbourhood
        best_neighbour = neighbours.get_best_neighbour(neighbourhood,initialState,last_van,tabu_memory,mutations_per_iteration)
        # update the initial state to the best neighbour
        initialState = best_neighbour.copy()
        
        # calculate the new time taken after swapping establishments
        new_time = time_utils.string_to_seconds((time_utils.total_time(initialState)))
        
         # check if the new time is better than the current best time
        if (new_time < best_time):
            # if so, update the best time and reset the counter
            best_time = new_time
            print("NEW BEST:" + time_utils.seconds_to_string(best_time))
            counter = 150
        else:
            # if not, decrement the counter
            counter -= 1
        
        # update the tabu memory
        update_tabu_memory(tabu_memory)
        # decrement the iterations counter
        iterations -= 1
   
    return initialState
