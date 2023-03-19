import networkx as nx
from datetime import datetime, timedelta

def is_open(establishment, hour):
    availableHours=eval(establishment['openingHours'])
    if (availableHours[hour]):
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


# format_time
def seconds_to_string(seconds):
    hours = (int)(seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_str = f"{hours}.{minutes:02.0f}.{seconds:02.0f}"

    return time_str


#time_to_seconds
def string_to_seconds(time_str):
    hours, minutes, seconds = time_str.split('.')

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds  

#time_to_hour
def string_hours(time_str):
    hours, _, _ = time_str.split('.')
    hours = int(hours)
    return hours


def total_time(solution, vanNum):
    return max([solution[i][-1][1] for i in range(vanNum)])


def waiting_time(graph,currentTime,establishment):

    hourAtArrival = (string_hours(seconds_to_string(currentTime)))%24  # hour at arrival on current node rounded down
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
        time = string_to_seconds(graph.edges[changedPath[i-1][0],changedPath[i][0]]['travelTime'])+string_to_seconds(changedPath[i-1][1])
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

        changedPath[i] = (changedPath[i][0],seconds_to_string(time))
    #print('alterado: ',changedPath)

    return changedPath


def arrival_time(prev_arrival_time, prev_establishment, inspection_time, travel_time):
    prev_arrival_hour = string_hours(prev_arrival_time)
    # waiting time
    if (not is_open(prev_establishment, prev_arrival_hour)):
        next_open_hour = next_open_hour(prev_establishment, prev_arrival_hour)
        if (next_open_hour < prev_arrival_hour):
            prev_arrival_time = 24 + next_open_hour
        else:
            prev_arrival_time = next_open_hour
        
        prev_arrival_seconds = prev_arrival_time*3600
        
    else:
        prev_arrival_seconds = string_to_seconds(prev_arrival_time)
    
    # inspection time + travel_t
    total_seconds = prev_arrival_seconds + inspection_time + travel_time
    arrival_time = seconds_to_string(total_seconds)
    return arrival_time 
