import time_utils as tu

def get_neighbourhood(graph,initialState):
    
    neighbourhood = []

    for i in range(len(initialState)):
        for j in range(1,len(initialState[i])):
            #print(initialState[i])
            for k in range(j+1,len(initialState[i])-1):
                neighbour = initialState[i].copy()
                neighbour[j] = initialState[i][k]
                neighbour[k] = initialState[i][j]
                neighbourhood.append(initialState[:i]+[tu.recalculate_hours(graph,neighbour)]+initialState[i+1:])



    return neighbourhood



