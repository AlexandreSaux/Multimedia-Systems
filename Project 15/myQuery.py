import tkinter as tk
from tkinter import *
from MergedPart.mySetValue import mySetValue
from MergedPart.myWindowInit import myWindowInit


def myQuery():
    # Initialize variables

    window = tk.Tk()
    myWindowInit(window)

    # Setup the window panel

    label = tk.Label(text="Please enter your query below")
    entry = tk.Entry(width=50)
    button = tk.Button(
        text="Click here to start refinement",
        width=25,
        height=1,
        command=lambda: mySetValue(entry, window)
    )
    label.place(relx=.5, rely=.465,anchor= CENTER)
    entry.place(relx=.5, rely=.5,anchor= CENTER)
    button.place(relx=.5, rely=.535,anchor= CENTER)
    window.mainloop()