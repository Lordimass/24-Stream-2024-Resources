from time import sleep
from datetime import datetime

def get_now_seconds(start):
    return int(start.strftime("%H"))*3600 + int(start.strftime("%M"))*60 + int(start.strftime("%S"))


print("Welcome to Lordimass' count down timer program, this was created as part of a set of programs and is designed to be used in parallel with OBS or Streamlabs, this program specifically creates a text file displaying a count down timer.")

valid = False
print("\nPlease enter a time for the timer to end at, in the format hh:mm, use 24hr time.")
while not valid:
    user_input = input()
    if not (":" in user_input):
        continue

    time = user_input.split(":")
    try:
        time[0] = int(time[0])
        time[1] = int(time[1])
        time.append(0)
        print(time)
    except:
        continue

    if time[0]<0 or time[0]>=24 or time[1]<0 or time[1]>=60:
        continue

    valid=True

start = datetime.now()
goal_seconds = time[0]*3600 + time[1]*60 + time[2]
now_seconds = get_now_seconds(start)

while now_seconds<goal_seconds:
    sleep(1)
    start = datetime.now()
    now_seconds = get_now_seconds(start)
    seconds_until = goal_seconds-now_seconds
    minutes_until = seconds_until//60
    seconds_until = seconds_until%60
    file = open("CountDown.txt", "w")
    output = str(minutes_until).rjust(2, "0")+":"+str(seconds_until).rjust(2, "0")
    print(output)
    file.write(output)
    file.close()

file = open("CountDown.txt", "w")
file.write("")
file.close()

