import networkx as nx
from datetime import datetime, timedelta


def is_open(establishment, hour):
    availableHours = eval(establishment['openingHours'])
    # print('hour: ', hour)
    # print('available hours: ', availableHours)
    if availableHours[hour % 24]:
        return True
    else:
        return False


def next_open_hour(establishment, hour):
    # Returns the next hour at which establishment is open given the arrival hour.
    # Find the next occurrence of 1 in the list after the given hour
    availableHours = eval(establishment['openingHours'])
    index = (hour % 24)
    while index < 24 and availableHours[index] == 0:
        index += 1
    if index == 24:  # No open hour found today, search for next open hour tomorrow
        index = 0
        while index < (hour % 24) and availableHours[index] == 0:
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


# time_to_seconds
def string_to_seconds(time_str):
    hours, minutes, seconds = time_str.split('.')

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds


# time_to_hour
def string_hours(time_str):
    # print(time_str)
    hours, _, _ = time_str.split('.')
    hours = int(hours)
    # print(hours%24)
    return hours


def total_time(solution):
    flat_list = [path[-1] for path in solution]
    # Find the maximum time value using max() function and a lambda function
    max_time = max(flat_list, key=lambda x: string_to_seconds(x[1]))

    return max_time#[1]


def waiting_time(graph, currentTime, establishment):
    hourAtArrival = (string_hours(seconds_to_string(currentTime))) % 24  # hour at arrival on current node rounded down
    # print(hourAtArrival)
    if (is_open(establishment, hourAtArrival)):
        waitingTime = 0
    else:
        next_open_seconds = next_open_hour(establishment, hourAtArrival) * 3600
        # ?waiting time could cross to the next day, so we need to check if the next open hour is after the current hour
        if (next_open_seconds > currentTime):
            waitingTime = (next_open_seconds - currentTime)
        else:
            waitingTime = ((24 * 3600) - (currentTime % (24 * 3600)) + next_open_seconds)

    # print('waiting time: ', waitingTime % 86400)
    return (waitingTime % 86400)


def recalculate_hours(graph, changedPath):
    # print('\nsem alteracao: ',changedPath)
    for i in range(1, len(changedPath)):
        time = string_to_seconds(graph.edges[changedPath[i - 1][0], changedPath[i][0]]['travelTime']) + string_to_seconds(changedPath[i - 1][1])
        waitingTime = waiting_time(graph, string_to_seconds(changedPath[i - 1][1]), graph.nodes[changedPath[i - 1][0]])

        if ((i - 1) != 0):
            time += waitingTime + (graph.nodes[changedPath[i - 1][0]]['inspectionDuration'])

        changedPath[i] = (changedPath[i][0], seconds_to_string(time))
    # print('alterado: ',changedPath)

    return changedPath


def arrival_time(prev_arrival_time, prev_establishment, inspection_time, travel_time):
    prev_arrival_hour = string_hours(prev_arrival_time)
    # waiting time
    if (not is_open(prev_establishment, prev_arrival_hour)):
        next_open = next_open_hour(prev_establishment, prev_arrival_hour)
        if next_open < (prev_arrival_hour % 24):
            prev_arrival_time = prev_arrival_hour + (24 -(prev_arrival_hour % 24)) + next_open
        else:
            prev_arrival_time = (prev_arrival_hour//24)*24 +  next_open

        prev_arrival_seconds = prev_arrival_time*3600
        
    else:
        prev_arrival_seconds = string_to_seconds(prev_arrival_time)

    # inspection time + travel_t
    total_seconds = prev_arrival_seconds + inspection_time + travel_time
    arrival_time = seconds_to_string(total_seconds)
    return arrival_time
