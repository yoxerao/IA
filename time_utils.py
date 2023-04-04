# checks if an establishment is open at a specific hour
def is_open(establishment, hour):
    availableHours = eval(establishment['openingHours'])
    if availableHours[hour % 24]:
        return True
    else:
        return False

# returns the next hour at which the establishment is open, given the arrival hour
def next_open_hour(establishment, hour):
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


# takes seconds and transforms them into the string hour.min.sec
def seconds_to_string(seconds):
    hours = (int)(seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_str = f"{hours}.{minutes:02.0f}.{seconds:02.0f}"

    return time_str


# takes the string hour.min.sec and transforms it into seconds
def string_to_seconds(time_str):
    hours, minutes, seconds = time_str.split('.')

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds


# takes the string and returns the hour
def string_hours(time_str):
    hours, _, _ = time_str.split('.')
    hours = int(hours)
    return hours

# calculates the time of a solution - the bigger arrival time amongst the vans
def total_time(solution):
    flat_list = [path[-1] for path in solution]
    max_time = max(flat_list, key=lambda x: string_to_seconds(x[1]))
    return max_time[1]


# knowing the time of arrival, calculates how long a van has to wait for the establishment to open
def waiting_time(graph, currentTime, establishment):
    hourAtArrival = (string_hours(seconds_to_string(currentTime))) % 24  # hour at arrival on current node rounded down
    if (is_open(establishment, hourAtArrival)):
        waitingTime = 0
    else:
        next_open_seconds = next_open_hour(establishment, hourAtArrival) * 3600
        # waiting time could cross to the next day, so we need to check if the next open hour is after the current hour
        if (next_open_seconds > currentTime):
            waitingTime = (next_open_seconds - currentTime)
        else:
            waitingTime = ((24 * 3600) - (currentTime % (24 * 3600)) + next_open_seconds)

    return (waitingTime % 86400)


# calculates the times for each node in the path based on the updated times of the previous nodes and the travel times between them
def recalculate_hours(graph, changedPath):
    for i in range(1, len(changedPath)):
        time = string_to_seconds(graph.edges[changedPath[i - 1][0], changedPath[i][0]]['travelTime']) + string_to_seconds(changedPath[i - 1][1])
        waitingTime = waiting_time(graph, string_to_seconds(changedPath[i - 1][1]), graph.nodes[changedPath[i - 1][0]])

        if ((i - 1) != 0):
            time += waitingTime + (graph.nodes[changedPath[i - 1][0]]['inspectionDuration'])

        changedPath[i] = (changedPath[i][0], seconds_to_string(time))

    return changedPath


# calculates the arrival time at an establishment, knowing the previous establishment infos and travel time between both establishments
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
