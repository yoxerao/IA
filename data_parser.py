import csv
import utils
import networkx as nx

def graph_establishments(sampleSize, graph):
    # open the file distance data file
    print("Parsing establishment data...")
    with open('data/establishments.csv', encoding="utf8") as csvEstablishments:
        # read the file
        reader = csv.reader(csvEstablishments)
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
                pred= -1,
                district=row[1], 
                county=row[2], 
                parish=row[3],
                address=row[4],
                latitude=float(row[5]), 
                longitude=float(row[6]), 
                inspectionUtility=float(row[7]), # urgência --> para desempate
                inspectionDuration=float(row[8])*60, # minutes to seconds
                openingHours=row[9]
            )
    
    print("Parsing distance data...")
    with open('data/distances.csv', encoding="utf8") as csvDistances:
        # read the file
        reader = csv.reader(csvDistances)

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
                    travelTime = float(val) # seconds
                    graph.add_edge(node1, node2, travelTime= utils.format_time(travelTime))
    print("Data parsed successfully!")
    return 0

    
