from requests import get
from bs4 import BeautifulSoup as bs
import datetime
import time
import random
import tkinter as tk
import threading

import dono_grabber
import overlay

min_wait = 30 # Time is in seconds
max_wait = 120
campaign_name = "24hr-stream-2024-reformation-fundraising"
remove_words = [",", " ", "£",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]    

def remove(string, removers):
    string = string.lower()
    for i in removers:
        string = string.replace(i,"")
    return int(string)

def scrape(campaign_name):
    URL = "https://www.gofundme.com/f/" + campaign_name
    headers = {'Accept-Language': 'en-UK,en;q=0.5'}
    page = get(URL, headers=headers)
    
    soup = bs(page.content, "html.parser")
    results = soup.find(id="__next")
    results = results.find("div", class_="campaign-layout_campaignPageLayout__5ojpo")
    results = results.find("div", class_="t-campaign-page-template")
    results = results.find("main", class_="t-campaign-page-template-content hrt-global-wrapper")
    results = results.find("div", class_="p-campaign")
    results = results.find("div", class_="p-campaign-sidebar")
    results = results.find("aside", class_="o-campaign-sidebar")
    results = results.find("div", class_="o-campaign-sidebar-wrapper")
    results = results.find("div", class_="")
    results = results.find("div", class_="progress-meter_progressMeter__ebbGu")
    results = results.find("div", class_="progress-meter_progressMeterHeading__7dug0")

    raised_result = results.find("div", class_="hrt-disp-inline")
    goal_result   = results.find("span", class_="hrt-text-body-sm hrt-text-gray")

    raised = remove(raised_result.text, remove_words)
    goal = remove(goal_result.text, remove_words)

    return raised, goal

def save(filename, data):
    file = open(filename + ".txt", "w", encoding="utf-8")
    file.write(str(data))
    file.close()

old_donos = dono_grabber.load_donos()
root = tk.Tk()
pb = overlay.SetUpPB(root)


def mainloop(old_donos, root, pb):
    time_start = time.perf_counter()
    
    # Updating progress towards goal
    donos = scrape(campaign_name)
    progress_text = f"£{donos[0]}/£{donos[1]}"
    save("raised", donos[0])
    save("goal", donos[1])
    save("progress_text", progress_text)

    # Updating Donation Cache and Latest/Highest Dono
    new_donos = dono_grabber.get_donos(campaign_name)
    combi_donos = dono_grabber.combine_donos(old_donos, new_donos)
    dono_grabber.update_cache(combi_donos)
    old_donos = combi_donos

    # Updating Progreess Bar
    overlay.update(pb)

    # Summarising Scrape
    time_end = time.perf_counter()
    time_taken = round((time_end - time_start)*(10^3))
    wait_time = random.randint(min_wait, max_wait)
    
    print(f"\nGoFundMe scraped successfully at: {datetime.datetime.now()}")
    print(f"    We have raised: £{donos[0]}")
    print(f"    of our goal of: £{donos[1]}")
    print(f"    Scrape took:    {time_taken}ms")
    print(f"    Waiting:        {wait_time}s")
    print("\n")
    
    root.after(wait_time*1000, mainloop, old_donos, root, pb)

mainloop(old_donos, root, pb)
root.mainloop()

