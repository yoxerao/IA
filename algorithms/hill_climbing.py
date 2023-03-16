import utils
import time_utils

def hillClimbing(graph,initialState,vans):
    
    local_maximum = False
    while(not(local_maximum)):
        neighbourhood = utils.get_neighbourhood(graph,initialState)
        for i in range(len(neighbourhood)):
            if(time_utils.total_time(neighbourhood[i],vans) < time_utils.total_time(initialState,vans)):
                print("FOUND ONE")
                print(time_utils.total_time(neighbourhood[i],vans))
                #print(neighbourhood[i])
                initialState = neighbourhood[i].copy()
                break
            if(i == len(neighbourhood)-1):
                local_maximum = True
    
    #print(initialState)
    return initialState

        