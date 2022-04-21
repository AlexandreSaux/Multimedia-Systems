import tkinter as tk
from tkinter import *
from MergedPart.mySetValueRefinement import mySetValueRefinement

def myQueryRefinement(window, freqs, myData):
    # Create a window to get user input

    window2 = tk.Toplevel(window)
    window2.title("Multimedia Systems Project 15")
    label = tk.Label(window2, text="Enter a term number to expand:")
    entry = tk.Entry(window2, width=50)
    button = tk.Button(
        window2,
        text="Submit",
        width=25,
        height=1,
        command=lambda: mySetValueRefinement(entry, window, window2, freqs)
    )
    label.pack(side=TOP, expand=YES)
    entry.pack(side=TOP, expand=YES)
    button.pack(side=TOP, expand=YES)
    window2.mainloop()