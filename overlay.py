import tkinter as tk
from tkinter import ttk
import ttkthemes as themes
import os
import time

def GetPercentage():
    goal = GetVal("goal.txt")
    raised = GetVal("raised.txt")
    return (raised/goal)*100

def GetVal(path):
    file = open(path, "r")
    val = int(file.read())
    file.close()
    return val

def RGBAImage(path):
    return Image.open(path).convert("RGBA")

def SetUpPB(root):
    print("Attempting to set up progress bar")
    progress_coords = (10,10)
    progress_thickness = 50
    progress_length = 280

    root.title("24hr Stream 2024 Overlay")
    root.geometry("300x70")
    root.resizable(False,False)
    root.configure(bg = "#ff00ff")

    s = ttk.Style()
    s.theme_use("default")
    s.configure("TProgressbar",
                thickness=progress_thickness,
                troughrelief = 'flat',
                background = "#1f9c23")

    pb = ttk.Progressbar(
        root,
        orient='horizontal',
        mode='determinate',
        length=progress_length,
        style = "TProgressbar",
    )

    pb.place(x = progress_coords[0],
             y = progress_coords[1])
    return pb

def update(pb):
    pb['value'] = GetPercentage()
    print("Updated overlay progress bar")
