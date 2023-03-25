import random
#import time_utils as tu
import networkx as nx


def calculate_random_paths(graph, departureTime, k, startNode):

    paths = [[] for _ in range(k)]
    nodesToVisit = list(graph.nodes())

    currentNodes = [startNode] * k  # each vehicle starts from the startNode
    arrivalTime = [departureTime] * k  # initialize arrivalTime for each vehicle to 9am

    for i in range(k):
        paths[i].append((startNode, tu.format_time(departureTime)))
    nodesToVisit.remove(startNode)

    while nodesToVisit:
        for i in range(k):
            currentNode = currentNodes[i]
            vehiclePath = paths[i]

            # check if there are no unvisited nodes left --> there's no more establishments to visit --> return to depot (starting point)
            if not nodesToVisit:
                for j in range(k):
                    if currentNodes[j] != startNode:
                        arrivalTime[j] += graph.nodes[currentNodes[j]]['inspectionDuration'] + tu.time_to_seconds(
                            graph.edges[currentNodes[j], startNode][
                                'travelTime'])  # add last inspection and travel time to startNode
                        paths[j].append((startNode, tu.format_time(
                            arrivalTime[j])))  # append startNode and final arrival time for each vehicle
                return paths

            # choose a random unvisited node for the current vehicle
            randomIndex = random.randint(0, len(nodesToVisit) - 1)
            nextNode = nodesToVisit[randomIndex]

            # calculate hour at arrival
            hourAtArrival = (tu.time_to_hour(tu.format_time(arrivalTime[i])))%24  # hour at arrival on current node rounded down
            # calculate the needed time to the chosen node
            travel_time = tu.time_to_seconds(graph.edges[currentNode, nextNode]['travelTime'])

            if currentNode == startNode:
                inspection_time = 0
                waiting_time = 0
            else:
                if (tu.is_open(graph.nodes[currentNode], hourAtArrival)):
                    waiting_time = 0
                    inspection_time = graph.nodes[currentNode]['inspectionDuration']
                else:
                    next_open_seconds = tu.next_open_hour(graph.nodes[currentNode], hourAtArrival) * 3600
                    # ?waiting time could cross to the next day, so we need to check if the next open hour is after the current hour
                    waiting_time = (next_open_seconds - arrivalTime[i]) if next_open_seconds > arrivalTime[i] else (
                                24 * 3600 - arrivalTime[i] + next_open_seconds)
                    inspection_time = graph.nodes[currentNode]['inspectionDuration']
            # update the arrival time, add the node to the path and remove it from the set of unvisited nodes
            print(" time at arrival: " + str(tu.format_time(arrivalTime[i])))
            print(" is the establishment " + str(currentNode) + " open? " + str(tu.is_open(graph.nodes[currentNode], hourAtArrival)))
            print(" waiting time: " + str(tu.format_time(waiting_time)))
            print(" inspection time: " + str(tu.format_time(inspection_time)))
            print(" travel time: " + str(tu.format_time(travel_time)) + "\n")
            arrivalTime[i] += travel_time + waiting_time + inspection_time

            vehiclePath.append((nextNode, tu.format_time(arrivalTime[i])))
            nodesToVisit.remove(nextNode)
            currentNodes[i] = nextNode  # update the current node for the current vehicle

    # if all nodes have been visited, append the start node and final arrival time for each vehicle
    for j in range(k):
        hourAtArrival = (tu.time_to_hour(tu.format_time(arrivalTime[j])))%24  # hour at arrival on current node rounded down
        # calculate the needed time to the chosen node
        travel_time = tu.time_to_seconds(graph.edges[currentNodes[j], startNode]['travelTime'])
        if currentNodes[j] == startNode:
            inspection_time = 0
            waiting_time = 0
        else:
            if (tu.is_open(graph.nodes[currentNodes[j]], hourAtArrival)):
                waiting_time = 0
                inspection_time = graph.nodes[currentNodes[j]]['inspectionDuration']
            else:
                next_open_seconds = tu.next_open_hour(graph.nodes[currentNodes[j]], hourAtArrival) * 3600
                # ?waiting time could cross to the next day, so we need to check if the next open hour is after the current hour
                waiting_time = (next_open_seconds - arrivalTime[j]) if next_open_seconds > arrivalTime[j] else (
                            24 * 3600 - arrivalTime[j] + next_open_seconds)
                inspection_time = graph.nodes[currentNodes[j]]['inspectionDuration']
            # update the arrival time, add the node to the path and remove it from the set of unvisited nodes
        print(" time at arrival: " + str(tu.format_time(arrivalTime[j])))
        print(" is the establishment " + str(currentNodes[j]) + " open? " + str(tu.is_open(graph.nodes[currentNodes[j]], hourAtArrival)))
        print(" waiting time: " + str(tu.format_time(waiting_time)))
        print(" inspection time: " + str(tu.format_time(inspection_time)))
        print(" travel time: " + str(tu.format_time(travel_time)))
        arrivalTime[j] += travel_time + waiting_time + inspection_time
        paths[j].append(
            (startNode, tu.format_time(arrivalTime[j])))  # append startNode and final arrival time for each vehicle

    return paths
