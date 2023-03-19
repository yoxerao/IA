import time_utils



def get_neighbourhood(graph,initialState):
    
    neighbourhood = []

    last_van = 0    # last van to finish
    max_time = 0

    for i, sublist in enumerate(initialState):
        for tup in sublist:
            if time_utils.string_to_seconds(tup[1]) > max_time:
                max_time = time_utils.string_to_seconds(tup[1])
                last_van = i

    #print(initialState)
    #print('\nlast van: ', last_van)

    #print('\n',initialState[last_van])

    for i in range(1,len(initialState[last_van])):
        for j in range(i+1,len(initialState[last_van])-1):
            neighbour = initialState[last_van].copy()
            neighbour[i] = initialState[last_van][j]
            neighbour[j] = initialState[last_van][i]
            neighbourhood.append(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour)]+initialState[last_van+1:])
            #print(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour)]+initialState[last_van+1:],'\n')


    #This for loop changes order os establishments in each van 
    # for i in range(len(initialState)):
    #     for j in range(1,len(initialState[i])):
    #         #print(initialState[i])
    #         for k in range(j+1,len(initialState[i])-1):
    #             neighbour = initialState[i].copy()
    #             neighbour[j] = initialState[i][k]
    #             neighbour[k] = initialState[i][j]
    #             neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour)]+initialState[i+1:])
                #print(neighbourhood)



    # This for loop changes establishments between 2 vans
    for i in range(len(initialState)):
        if(i == last_van):
            continue
        for j in range(1,len(initialState[last_van])-1):
            for k in range(1,len(initialState[i])-1):
                neighbour1 = initialState[last_van].copy()
                neighbour2 = initialState[i].copy()
                #print('\n\nn1: ',neighbour1)
                #print('n2: ',neighbour2)
                neighbour1[j] = initialState[i][k]
                neighbour2[k] = initialState[last_van][j]
                #print('\nnew n1: ',neighbour1)
                #print('new n2: ',neighbour2)

                if (i < last_van):
                    neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:])
                    #print(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:],'\n')
                    #print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
                    #print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))
                else:
                    neighbourhood.append(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:])
                    #print(initialState[:last_van]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[last_van+1:i]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[i+1:],'\n')
                    #print('\nnew time n1: ',time_utils.recalculate_hours(graph,neighbour1))
                    #print('new time n2: ',time_utils.recalculate_hours(graph,neighbour2))



    # This for loop changes establishments between 2 vans
    # for i in range(len(initialState)-1):
    #     for j in range(i+1,len(initialState)):
    #         for k in range(1,len(initialState[i])-1):
    #             for l in range(1,len(initialState[j])-1):

    #                 neighbour1 = initialState[i].copy()
    #                 neighbour2 = initialState[j].copy()
    #                 #if (j <= 1):
    #                     #print('\n\nn1: ',neighbour1)
    #                     #print('n2: ',neighbour2)

    #                 neighbour1[k] = initialState[j][l]
    #                 neighbour2[l] = initialState[i][k]
    #                 neighbourhood.append(initialState[:i]+[time_utils.recalculate_hours(graph,neighbour1)]+initialState[i+1:j]+[time_utils.recalculate_hours(graph,neighbour2)]+initialState[j+1:])
                

    print(len(neighbourhood))

    return neighbourhood



