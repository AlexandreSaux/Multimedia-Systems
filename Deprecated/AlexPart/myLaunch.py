import tkinter as tk
from tkinter import *
from AlexPart.myRequest import myRequest
from AlexPart.mySetValue import mySetValue

def myLaunch():
    window = tk.Tk()
    window.title("Multimedia Systems Project 15")
    label = tk.Label(text="Please enter your query below")
    entry = tk.Entry(width=50)
    button = tk.Button(
        text="Click here to start refinement",
        width=25,
        height=1,
        command=lambda: mySetValue(entry, window)
    )
    label.pack(side=TOP, expand=YES)
    entry.pack(side=TOP, expand=YES)
    button.pack(side=TOP, expand=YES)
    window.geometry("500x200")
    window.mainloop()
    myRequest()