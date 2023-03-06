import csv

# open the file distance data file
with open('data/distances.csv', 'r') as f:
    # read the file
    reader = csv.reader(f)
    # skip the header
    next(reader, None)
    # read the rest of the data
    #...
    