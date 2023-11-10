import time

def marketHours():
    day = time.gmtime().tm_wday 
    hour = time.gmtime().tm_hour + 1
    minute = time.gmtime().tm_min
    if day >= 0 and day <= 4:
        if hour == 14 and minute >= 30:
            return True
        elif 14 < hour < 21:
            return True
        else: 
            return False
    else: 
        return False
    
def getTransacTime():
    current_time = time.time()
    current_time = time.gmtime(current_time)
    time_str = f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}"
    return time_str

def getTransacDate():
    current_time = time.time()
    current_time = time.gmtime(current_time)
    date_str = f"{current_time.tm_mon}/{current_time.tm_mday}/{current_time.tm_year}"
    return date_str