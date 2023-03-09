import random
import networkx as nx

def calculate_random_paths(graph, k, startNode): #!!! OPENING HOURS NOT IMPLEMENTED !!!
    paths = [[] for _ in range(k)]
    nodesToVisit = set(graph.nodes())
    
    currentNodes = [startNode] * k # each vehicle starts from the startNode
    arrivalTime = [9*60] * k # initialize arrivalTime for each vehicle to 9am

    for i in range(k):
        paths[i].append((startNode, round(arrivalTime[i]/60,2)))
    nodesToVisit.remove(startNode)

    while nodesToVisit:
        for i in range(k):
            currentNode = currentNodes[i]
            vehiclePath = paths[i]

            # find the unvisited nodes
            unvisitedNodes = list(nodesToVisit)

            # check if there are no unvisited nodes left
            if not unvisitedNodes:
                for j in range(k):
                    if currentNodes[j] != startNode:
                        arrivalTime[j] += graph.nodes[currentNodes[j]]['inspectionDuration'] + graph[currentNodes[j]][startNode]['travelTime'] #add last inspection and travel time to startNode
                        paths[j].append((startNode, round(arrivalTime[j]/60,2)))  # append startNode and final arrival time for each vehicle
                return paths

            # choose a random unvisited node for the current vehicle
            randomIndex = random.randint(0, len(unvisitedNodes) - 1)
            nextNode = unvisitedNodes[randomIndex]

            # calculate the needed time to the chosen node
            travel_time = graph[currentNode][nextNode]['travelTime']
            if currentNode == startNode:
                inspection_time = 0
            else:
                inspection_time = graph.nodes[currentNode]['inspectionDuration']
            # update the arrival time, add the node to the path and remove it from the set of unvisited nodes
            arrivalTime[i] += travel_time + inspection_time
            vehiclePath.append((nextNode, round(arrivalTime[i]/60,2)))
            nodesToVisit.remove(nextNode)
            currentNodes[i] = nextNode  # update the current node for the current vehicle

    # if all nodes have been visited, append the start node and final arrival time for each vehicle
    for j in range(k):
        if currentNodes[j] != startNode:
            arrivalTime[j] += graph.nodes[currentNodes[j]]['inspectionDuration'] + graph[currentNodes[j]][startNode]['travelTime'] #add last inspection and travel time to startNode
            paths[j].append((startNode, round(arrivalTime[j]/60,2)))  # append startNode and final arrival time for each vehicle
    return paths