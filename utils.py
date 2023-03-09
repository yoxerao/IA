import networkx as nx


def is_open(establishment, time):
    openingHours=eval(establishment['openingHours'])
    if (openingHours[time]):
        return True 
    else:
        return False