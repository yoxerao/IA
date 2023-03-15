import networkx as nx


def is_open(establishment, time):
    openingHours=eval(establishment['openingHours'])
    if (openingHours[time]):
        return True 
    else:
        return False
    

def format_time(seconds):
    
    hours = (int)(seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    
    time_str = f"{hours}.{minutes:02.0f}.{seconds:02.0f}"

    return time_str



def time_to_seconds(time_str):
    
    hours, minutes, seconds = time_str.split('.')

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds   

def total_time(solution, vanNum):
    return max([solution[i][-1][1] for i in range(vanNum)])