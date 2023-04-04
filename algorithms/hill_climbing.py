import time_utils
import neighbours

def hillClimbing(graph,initialState):
    local_maximum = False
    
    # continue searching for solutions until a local maximum is reached
    while(not(local_maximum)):
        last_van = 0  # last van to finish
        max_time = 0 # maximum time taken
        
        # update last_van and max_time in case a new maximum is found
        for i, sublist in enumerate(initialState):
            for tup in sublist:
                if time_utils.string_to_seconds(tup[1]) > max_time:
                    max_time = time_utils.string_to_seconds(tup[1])
                    last_van = i
        
        # generate a new neighbour solution by swapping establishments within the last van
        new_neighbour = neighbours.swap_establishments_in_van(graph,initialState,last_van)
        
        # if a new neighbour is found, update the current solution and continue searching
        if(len(new_neighbour) != 0):
            print("FOUND ONE INSIDE VAN")
            print(time_utils.total_time(new_neighbour))
            initialState = new_neighbour.copy()
            continue
        
        # generate a new neighbour solution by swapping establishments between the last van and another van
        new_neighbour = neighbours.swap_establishments_between_van(graph, initialState,last_van)
        
        # if a new neighbour is found, update the current solution and continue searching
        if(len(new_neighbour) != 0):
            print("FOUND ONE BETWEEN TWO VANS")
            print(time_utils.total_time(new_neighbour))
            initialState = new_neighbour.copy()
            continue
        
        # if no new neighbour is found, set local_maximum flag to True to terminate the search
        local_maximum = True

    # return the final solution
    return initialState    