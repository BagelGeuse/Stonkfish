import apilib
import pytz
import datetime
import time
import timesToRequest
import sys
import sched
import subprocess

eastern = pytz.timezone("US/Eastern")
iterator = 0

s = sched.scheduler(time.time, time.sleep)

def getNextTime(iterator):
    local_dt = eastern.localize(datetime.datetime.now())
    str_diff = local_dt.strftime("%z")

    int_diff = int(str_diff[0:3])*60*60

    nextInterval = int(time.time())

    nextInterval += int_diff   
    remainder = nextInterval % 86400
    nextInterval -= remainder
    nextInterval += timesToRequest.times[iterator]
    nextInterval -= int_diff

    return nextInterval

def updateStockData(i):
    ticker = subprocess.check_output(f"python apilib.py getTickerFromID {i}", shell=True)[:-1].decode("ascii")
    print(f"Ticker {ticker}")
    
    if(ticker == "None"):
        return "No Ticker"
    
    response = subprocess.check_output(f"python apilib.py getStockData {ticker}", shell=True)[:-1].decode("ascii")
    print(f"    Data fetch: {'Failure' if response == 'Error' else 'Success'}")
    
    if(response == "Error"):
        return "API Error"

    subprocess.check_output(f"python apilib.py compileR {ticker}", shell=True)
    subprocess.check_output(f"python apilib.py storeResult {ticker}", shell=True)
    print(f"    Compiled and saved data")

    return "Success"

def executeSchedule(i):

    print("--------------------------------------------------")
    print(f"Execute happened at {time.time()}; {datetime.datetime.fromtimestamp(time.time(), eastern).strftime('%Y-%m-%d %H:%M:%S')}")
    print("--------------------------------------------------")
    print(f"Times List Index: {i}")

    updateStockData(i)

    newI = (i+1)%192
    
    dayTime = timesToRequest.times[newI]
    nextTime =  getNextTime(newI)

    if(timesToRequest.times[newI] < timesToRequest.times[i]):
        nextTime += 86400
        #the get next time fn doesnt account for changes in the day

    print(f"Waiting for dayTime {dayTime}; unixtime {nextTime}; {datetime.datetime.fromtimestamp(nextTime, eastern).strftime('%Y-%m-%d %H:%M:%S')}")
    s.enterabs(nextTime, 10, lambda: executeSchedule(newI))
    s.run()


# print(getNextTime(int(sys.argv[1])))

if(sys.argv[1] == "start"):
    executeSchedule(int(sys.argv[2]))

if(sys.argv[1] == "get"):
    print(timesToRequest.times2.index(int(sys.argv[2])))

if(sys.argv[1] == "test"):
    print(test())