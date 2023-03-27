import random
import time_utils as tu
import networkx as nx


def calculate_random_paths(graph, departureTime, k, startNode):
    paths = [[] for _ in range(k)]
    nodesToVisit = list(graph.nodes())

    currentNodes = [startNode] * k  # each vehicle starts from the startNode
    arrivalTime = [departureTime] * k  # initialize arrivalTime for each vehicle to 9am

    for i in range(k):
        paths[i].append((startNode, departureTime))

    nodesToVisit.remove(startNode)

    while nodesToVisit:
        # choose a random vehicle
        random_van = random.randint(0, k - 1)
        currentNode = currentNodes[random_van]
        vanPath = paths[random_van]

        # choose a random unvisited node for the current vehicle
        randomIndex = random.randint(0, len(nodesToVisit) - 1)
        nextNode = nodesToVisit[randomIndex]

        inspection_time = graph.nodes[currentNode]['inspectionDuration'] if currentNode != startNode else 0
        travel_time = tu.string_to_seconds(graph.edges[currentNode, nextNode]['travelTime'])
        # calculate the arrival time for the chosen node
        arrivalTime[random_van] = tu.arrival_time(arrivalTime[random_van], graph.nodes[currentNode], inspection_time, travel_time)

        vanPath.append((nextNode, arrivalTime[random_van]))
        currentNodes[random_van] = nextNode  # update the current node for the current vehicle
        nodesToVisit.remove(nextNode)

    # if all nodes have been visited, append the start node and final arrival time for each vehicle
    for j in range(k):
        # calculate the needed time to the chosen node
        travel_time = tu.string_to_seconds(graph.edges[currentNodes[j], startNode]['travelTime'])
        inspection_time = graph.nodes[currentNodes[j]]['inspectionDuration'] if currentNodes[j] != startNode else 0

        arrivalTime[j] = tu.arrival_time(arrivalTime[j], graph.nodes[currentNodes[j]], inspection_time, travel_time)
        paths[j].append((startNode, arrivalTime[j]))  # append startNode and final arrival time for each vehicle

    return paths
