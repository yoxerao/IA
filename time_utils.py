import networkx as nx

def is_open(establishment, time):
    availableHours=eval(establishment['openingHours'])
    if (availableHours[time]):
        return True 
    else:
        return False

def next_open_hour(establishment, hour):
    #Returns the next hour at which establishment is open given the arrival hour.
    # Find the next occurrence of 1 in the list after the given hour
    availableHours=eval(establishment['openingHours'])
    index = hour
    while index < 24 and availableHours[index] == 0:
        index += 1
    if index == 24:  # No open hour found today, search for next open hour tomorrow
        index = 0
        while index < hour and availableHours[index] == 0:
            index += 1
    # Calculate the number of hours until the establishment is open
    return index 


def format_time(seconds):
    
    hours = (int)(seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    
    time_str = f"{hours}.{minutes:02.0f}.{seconds:02.0f}"

    return time_str



def time_to_seconds(time_str):
    
    hours, minutes, seconds = time_str.split('.')

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds   

def time_to_hour(time_str):
    
    hours, minutes, seconds = time_str.split('.')

    hours = int(hours)

    return hours

def total_time(solution, vanNum):
    return max([solution[i][-1][1] for i in range(vanNum)])


def waiting_time(graph,currentTime,establishment):

    hourAtArrival = (time_to_hour(format_time(currentTime)))%24  # hour at arrival on current node rounded down
    #print(hourAtArrival)
    if (is_open(establishment, hourAtArrival)):
        waitingTime = 0
    else:
        next_open_seconds = next_open_hour(establishment, hourAtArrival) * 3600
        # ?waiting time could cross to the next day, so we need to check if the next open hour is after the current hour
        waitingTime = (next_open_seconds - currentTime) if next_open_seconds > currentTime else ((24 * 3600) - (currentTime % (24*3600)) + next_open_seconds)
    
     
    return (waitingTime % 86400)


def recalculate_hours(graph,changedPath):
    #print('sem alteracao: ',changedPath)
    for i in range(1,len(changedPath)):
        time = time_to_seconds(graph.edges[changedPath[i-1][0],changedPath[i][0]]['travelTime'])+time_to_seconds(changedPath[i-1][1])
        # if(i == 2):

        #     if(waiting_time(graph,time,graph.nodes[changedPath[i+1][0]]) != 0):
        #         print('\n')
        #         print('origin: ',changedPath[i][0])
        #         print('destination: ',changedPath[i+1][0])
        #         print(format_time(time))
        #         print(waiting_time(graph,time,graph.nodes[changedPath[i+1][0]])) 
        if ((i-1) == 0):
            time += waiting_time(graph,time,graph.nodes[changedPath[i][0]])
        else:
            time += (graph.nodes[changedPath[i-1][0]]['inspectionDuration']) + waiting_time(graph,time,graph.nodes[changedPath[i][0]])

        changedPath[i] = (changedPath[i][0],format_time(time))
    #print('alterado: ',changedPath)

    return changedPath


