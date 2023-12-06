import csv
import requests
from time import sleep
import random
from forex_python.converter import CurrencyRates


def get_donos(campaign_name):
    c = CurrencyRates()
    donos = []
    comments_url = "https://gateway.gofundme.com/web-gateway/v1/feed/"+ campaign_name +"/donations"
    
    params = {"limit": 10, "offset": 0}
    data = requests.get(comments_url, params=params).json()
    
    for dono in data["references"]["donations"]:
        amount  = dono["amount"]
        currency = dono["currencycode"]
        name    = dono["name"]
        time    = dono["created_at"]

        if currency != "GBP":
            print("Converting from {currency} to GBP")
            amount = c.convert(currency, "GBP", amount)
        
        dono = [name, float(amount), time]
        donos.append(dono)

    return donos

def load_donos():
    try:
        donos = []
        file = open("cached_donos.csv", "r")
        reader = csv.reader(file)    
        for line in reader:
            line[1] = float(line[1])
            donos.append(line)
        file.close()
        return donos
    except Exception as e: # No cache exists
        print(e)
        return []

def combine_donos(old_donos, new_donos):
    for dono in new_donos:
        if not(dono in old_donos):
            old_donos.append(dono)
            print("New donation: " + str(dono))
            update_highest(dono)
            update_latest(dono)

    return old_donos

def update_cache(donos):
    file = open("cached_donos.csv", "w", newline='')
    writer = csv.writer(file)
    for row in donos:
        writer.writerow(row)

def wait_rand_time(lowest, highest):
    time = random.randint(lowest,highest)
    print(f"Waiting {time} seconds before next scrape \n")
    sleep(random.randint(lowest,highest))

def overwrite(path, content):
    file = open(path, "w", encoding="utf-8")
    file.write(content)
    file.close()

def update_highest(dono):
    try:
        file = open("Highest Dono/amount.txt", "r")
        amount = float(file.readline().strip("£"))
        file.close()
    except Exception as e:
        print("Highest amount not found, using 0")
        print(e)
        amount = 0

    if dono[1]<amount:
        return None

    overwrite("Highest Dono/amount.txt", format(dono[1], ".2f"))
    overwrite("Highest Dono/name.txt", dono[0])
    overwrite("Highest Dono/display.txt", dono[0] + " • £" + format(dono[1], ".2f"))

def update_latest(dono):
    overwrite("Last Dono/amount.txt", format(dono[1], ".2f"))
    overwrite("Last Dono/name.txt", dono[0])
    overwrite("Last Dono/display.txt", dono[0] + " • £" + format(dono[1], ".2f"))

# Old code used to run this script independently of main.py
'''old_donos = load_donos()
print("Loaded cached donos from file\n")
#print(old_donos)
while True:
    new_donos = get_donos()
    combi_donos = combine_donos(old_donos, new_donos)
    update_cache(combi_donos)
    print("Scrape complete")
    wait_rand_time(60,120)
    old_donos = combi_donos'''
