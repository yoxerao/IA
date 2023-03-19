import time_utils
import random

def get_neighbourhood(graph,initialState):
    
    neighbourhood = []


    # This for loop changes order os establishments in each van 
    for i in range(len(initialState)):
        for j in range(1,len(initialState[i])):
            #print(initialState[i])
            for k in range(j+1,len(initialState[i])-1):
                neighbour = initialState[i].copy()
                neighbour[j] = initialState[i][k]
                neighbour[k] = initialState[i][j]
                neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour)]+initialState[i+1:])
                #print(neighbourhood)


    # This for loop changes establishments between 2 vans
    for i in range(len(initialState)-1):
        for j in range(i+1,len(initialState)):
            for k in range(1,len(initialState[i])-1):
                for l in range(1,len(initialState[j])-1):

                    neighbour1 = initialState[i].copy()
                    neighbour2 = initialState[j].copy()
                    #if (j <= 1):
                        #print('\n\nn1: ',neighbour1)
                        #print('n2: ',neighbour2)

                    neighbour1[k] = initialState[j][l]
                    neighbour2[l] = initialState[i][k]
                    neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[i+1:j]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[j+1:])
                

                

    return neighbourhood


