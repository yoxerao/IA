import csv
import sqlite3

# open the file
with open('line_color.csv' , encoding="utf8") as csvfile:
    # create the object of csv.reader()
    csv_file_reader = csv.reader(csvfile,delimiter=';')
    # skip the header 
    next(csv_file_reader,None)
    
    # 2. create database
    connection=sqlite3.connect('database.db')
    curosr=connection.cursor()
    # 4. pase csv data
    for row in csv_file_reader:
        # skip the first row
        for i in range(len(row)):
            # assign each field its value
            id=row[0]
            name=row[1]
            hex_code=row[2]

        # 5. create insert query
        InsertQuery='''INSERT INTO Line_color VALUES (?, ?, ?)'''
        # 6. Execute query
        curosr.execute(InsertQuery, (id, name, hex_code))
    # 7. commit changes
    connection.commit()
    # 8. close connection
    connection.close()

# open the file
with open('lines.csv' , encoding="utf8") as csvfile:
    # create the object of csv.reader()
    csv_file_reader = csv.reader(csvfile,delimiter=';')
    # skip the header 
    next(csv_file_reader,None)
    
    # 2. create database
    connection=sqlite3.connect('database.db')
    curosr=connection.cursor()
    # 4. pase csv data
    for row in csv_file_reader:
        # skip the first row
        for i in range(len(row)):
            # assign each field its value
            id=row[0]
            code=row[3]
            go_name=row[5]
            return_name=row[6]
            id_line_color = row[7]
        
        # 5. create insert query
        InsertQuery='''INSERT INTO Line VALUES (?, ?, ?, ?, ?)'''
        # 6. Execute query
        curosr.execute(InsertQuery, (id, code, go_name, return_name, id_line_color))
    # 7. commit changes
    connection.commit()
    # 8. close connection
    connection.close()
    
    # open the file
with open('stops.csv' , encoding="utf8") as csvfile:
    # create the object of csv.reader()
    csv_file_reader = csv.reader(csvfile,delimiter=';')
    # skip the header 
    next(csv_file_reader,None)
    
    # 2. create database
    connection=sqlite3.connect('database.db')
    curosr=connection.cursor()
    # 4. pase csv data
    for row in csv_file_reader:
        # skip the first row
        for i in range(len(row)):
            # assign each field its value
            id=row[0]
            code=row[1]
            is_active=row[3]
            name=row[4]
            latitude = row[5]
            longitude = row[6]
            map_point = row[7]
        
        # 5. create insert query
        InsertQuery='''INSERT INTO Stop VALUES (?, ?, ?, ?, ?, ?, ?)'''
        # 6. Execute query
        curosr.execute(InsertQuery, (id, code, is_active, name, latitude, longitude, map_point))
    # 7. commit changes
    connection.commit()
    # 8. close connection
    connection.close()
    
    # open the file
with open('paths.csv' , encoding="utf8") as csvfile:
    # create the object of csv.reader()
    csv_file_reader = csv.reader(csvfile,delimiter=';')
    # skip the header 
    next(csv_file_reader,None)
    
    # 2. create database
    connection=sqlite3.connect('database.db')
    curosr=connection.cursor()
    # 4. pase csv data
    for row in csv_file_reader:
        # skip the first row
        for i in range(len(row)):
            # assign each field its value
            id=row[0]
            code=row[2]
            orientation=row[3]
            id_line = row[4]

        
        # 5. create insert query
        InsertQuery='''INSERT INTO Path VALUES (?, ?, ?, ?)'''
        # 6. Execute query
        curosr.execute(InsertQuery, (id, code, orientation, id_line))
    # 7. commit changes
    connection.commit()
    # 8. close connection
    connection.close()
    
    # open the file
with open('paths_stops.csv' , encoding="utf8") as csvfile:
    # create the object of csv.reader()
    csv_file_reader = csv.reader(csvfile,delimiter=';')
    # skip the header 
    next(csv_file_reader,None)
    
    # 2. create database
    connection=sqlite3.connect('database.db')
    curosr=connection.cursor()
    # 4. pase csv data
    for row in csv_file_reader:
        # skip the first row
        for i in range(len(row)):
            # assign each field its value
            id=row[0]
            stop_order=row[2]
            id_stop=row[4]
            id_path = row[3]

        # 5. create insert query
        InsertQuery='''INSERT INTO Path_stop VALUES (?, ?, ?, ?)'''
        # 6. Execute query
        curosr.execute(InsertQuery, (id, stop_order, id_stop, id_path))
    # 7. commit changes
    connection.commit()
    # 8. close connection
    connection.close()