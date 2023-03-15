


#def recalculate_time(start, newPath):




def get_neighbourhood(initialState):
    
    neighbourhood = []

    for i in range(len(initialState)):
        for j in range(1,len(initialState[i])):
            #print(initialState[i])
            for k in range(j+1,len(initialState[i])):
                neighbour = initialState[i].copy()
                neighbour[j] = initialState[i][k]
                neighbour[k] = initialState[i][j]
                neighbourhood.append(initialState[:i]+[neighbour]+initialState[i+1:])

    print (len(neighbourhood))

    return neighbourhood

#get_neighbourhood([[(0, 9.0), (195, 9.18), (544, 10.34), (819, 12.8), (894, 14.09), (528, 14.77), (533, 15.77), (934, 17.04), (65, 18.74), (301, 20.92), (808, 22.52), (0, 24.49)], [(0, 9.0), (370, 9.59), (119, 12.42), (554, 14.8), (200, 17.29), (828, 19.94), (31, 22.28), (218, 24.62), (23, 25.36), (910, 26.51), (968, 27.44), (0, 28.32)],[(444,555),(666,777)]])