import csv
import networkx as nx

def graph_establishments(sampleSize, graph):
    # open the file distance data file
    print("Parsing establishment data...")
    with open('data/establishments.csv', encoding="utf8") as csv_establishments:
        # read the file
        reader = csv.reader(csv_establishments)
        # skip the header
        next(reader, None)
        # read the rest of the data
        acc = 0
        for row in reader:
            if acc > sampleSize-1:
                break
            acc+=1
            graph.add_node(
                int(row[0]), 
                district=row[1], 
                county=row[2], 
                parish=row[3], 
                address=row[4], 
                latitude=float(row[5]), 
                longitude=float(row[6]), 
                inspectionUtility=float(row[7]), 
                inspectionDuration=float(row[8])*60, 
                openingHours=row[9]
            )
    
    print("Parsing distance data...")
    with open('data/distances.csv', encoding="utf8") as csv_distances:
        # read the file
        reader = csv.reader(csv_distances)

        for i, row in enumerate(reader):
            if i == 0:
                continue
            if i > sampleSize:
                break
            node1 = i-1  # Get the first node id
            for j, val in enumerate(row[1:]):  
                if j > sampleSize - 1:
                    break
                if val != '0':  # Only add edges with non-zero values
                    node2 = j  # Get the second node id
                    time = float(val)  
                    graph.add_edge(node1, node2, travelTime=time)  # Add the edge to the graph with the time attribute
    print("Data parsed successfully!")
    return 0

    
