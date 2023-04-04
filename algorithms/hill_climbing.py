import time_utils
import neighbours

def hillClimbing(graph,initialState):
    
    local_maximum = False
    while(not(local_maximum)):
        last_van = 0  # last van to finish
        max_time = 0

        for i, sublist in enumerate(initialState):
            for tup in sublist:
                if time_utils.string_to_seconds(tup[1]) > max_time:
                    max_time = time_utils.string_to_seconds(tup[1])
                    last_van = i
        new_neighbour = neighbours.swap_establishments_in_van(graph,initialState,last_van)

        if(len(new_neighbour) != 0):
            print("FOUND ONE INSIDE VAN")
            print(time_utils.total_time(new_neighbour))
            initialState = new_neighbour.copy()
            continue

        new_neighbour = neighbours.swap_establishments_between_van(graph, initialState,last_van)

        if(len(new_neighbour) != 0):
            print("FOUND ONE BETWEEN TWO VANS")
            print(time_utils.total_time(new_neighbour))
            initialState = new_neighbour.copy()
            continue
        
        local_maximum = True

    return initialState

        