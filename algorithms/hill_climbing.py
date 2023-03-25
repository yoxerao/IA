import utils
import time_utils

def hillClimbing(graph,initialState,vans):
    
    local_maximum = False
    while(not(local_maximum)):
        last_van = 0  # last van to finish
        max_time = 0

        for i, sublist in enumerate(initialState):
            for tup in sublist:
                if time_utils.string_to_seconds(tup[1]) > max_time:
                    max_time = time_utils.string_to_seconds(tup[1])
                    last_van = i
        new_neighbour = utils.swap_establishments_in_van(graph,initialState,last_van)

        if(len(new_neighbour) != 0):
            print("FOUND ONE INSIDE VAN")
            print(time_utils.total_time(new_neighbour))
            initialState = new_neighbour.copy()
            continue

        new_neighbour = utils.swap_establishments_between_van(graph, initialState,last_van)

        if(len(new_neighbour) != 0):
            print("FOUND ONE BETWEEN TWO VANS")
            print(time_utils.total_time(new_neighbour))
            initialState = new_neighbour.copy()
            continue

        # neighbourhood = utils.get_neighbourhood(graph,initialState)
        # for i in range(len(neighbourhood)):
        #     if(time_utils.string_to_seconds(time_utils.total_time(neighbourhood[i])[1]) < time_utils.string_to_seconds(time_utils.total_time(initialState)[1])):
        #         print('old best time:',time_utils.total_time(initialState))
        #         print('new best time:',time_utils.total_time(neighbourhood[i]))
        #         print("FOUND ONE")
        #         print(time_utils.total_time(neighbourhood[i]))
        #         #print(neighbourhood[i])
        #         initialState = neighbourhood[i].copy()
        #         break
        #     if(i == len(neighbourhood)-1):
        
        local_maximum = True
    
    #print('\n\n',initialState)
    return initialState

        