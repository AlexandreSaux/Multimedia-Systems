import tkinter as tk
from tkinter import *
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.destroyWindow import destroyWindow

def myRefinementSecondCase(term, window):
    # If there is no alternative make a simple popup

    myRefinement = "No alternative senses found for term \"" + term + "\"\n"
    window2 = tk.Toplevel(window)
    window2.title("Multimedia Systems Project 15")
    label = tk.Label(window2, text=myRefinement)
    entry = tk.Entry(window2, width=50)
    button = tk.Button(
        window2,
        text="Understood",
        width=25,
        height=1,
        command=lambda: destroyWindow(window2)
    )
    label.pack(side=TOP, expand=YES)
    entry.pack(side=TOP, expand=YES)
    button.pack(side=TOP, expand=YES)
    window2.mainloop()
    myGlobalInit.myQuery = myGlobalInit.myQuery + " " + term