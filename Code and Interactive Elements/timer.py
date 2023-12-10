import time
from datetime import datetime

print("Welcome to Lordimass' timer program, this was created as part of a set of programs and is designed to be used in parallel with OBS or Streamlabs, this program specifically creates a text file displaying a count up timer.")

# Finding cache
try:
    file = open("timer.txt")
    timer = file.readline()
    time_list = timer.split(":")
    file.close()
    usecache = True
except:
    usecache = False

# Asking user whether to use cache
if usecache:
    print("I found a cached timer value, would you like to use this one [1] or start a new timer [2]?")
    valid = False
    while not valid:
        usecache = input()
        if usecache == "1":
            usecache = True
            valid = True
        elif usecache == "2":
            usecache = False
            valid = True
        else:
            print("I didn't recognise that input, try entering either 1 or 2")
else:
    print("I didn't find an existing timer value, so I'll start a timer from 0")

if not usecache:
    file = open("timer.txt", "w")
    timer = "00:00:00"
    time_list = timer.split(":")
    file.write("00:00:00")
    file.close()


time_list = [int(time_list[0]),int(time_list[1]),int(time_list[2])]

input("\nPress enter when you're ready to begin the timer.")
start = datetime.now()
while True:
    time.sleep(1)
    
    now = datetime.now()
    time_list[2] += (int(now.strftime("%S")) - int(start.strftime("%S")))%60
    start = now
    
    if time_list[2] >= 60:
        time_list[1] += time_list[2]//60
        time_list[2] = time_list[2]%60
        print(time_list)

    if time_list[1] >= 60:
        time_list[0] += time_list[1]//60
        time_list[1] = time_list[1]%60

    secs  = str(time_list[0]).rjust(2, "0")
    mins  = str(time_list[1]).rjust(2, "0")
    hours = str(time_list[2]).rjust(2, "0")

    timer = secs + ":" + mins + ":" + hours

    file = open("timer.txt", "w")
    file.write(timer)
    file.close()
