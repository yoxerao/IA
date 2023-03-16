import networkx as nx


def is_open(establishment, time):
    openingHours=eval(establishment['openingHours'])
    rounded_time = (time // 3600) % 24
    if (openingHours[rounded_time]):
        return True 
    else:
        return False