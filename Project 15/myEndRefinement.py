import tkinter as tk
from tkinter import *
import MergedPart.myGlobalInit as myGlobalInit

def myEndRefinement(window, mySearchResults, myHistogram):
    # Create a window to get user input

    window.destroy()
    window2 = tk.Tk()
    window2.state("zoomed")
    window2.title("Multimedia Systems Project 15")
    leftFrame = Frame(window2)
    rightFrame = Frame(window2)
    leftFrame.pack(side=LEFT, expand=YES)
    rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
    initQuery = tk.Label(text="Your initial query: " + myGlobalInit.initialQuery)
    initResult = tk.Label(text=myGlobalInit.initialResult)
    initHistogram = tk.Label(text=myGlobalInit.initialHistogram, justify=LEFT)
    finalQuery = tk.Label(text="Your final query: " + myGlobalInit.myQuery)
    finalResult = tk.Label(text=mySearchResults)
    finalHistogram = tk.Label(text=myHistogram, justify=LEFT)
    initQuery.pack(in_=leftFrame, side=TOP, expand=YES)
    initResult.pack(in_=leftFrame, side=TOP, expand=YES)
    initHistogram.pack(in_=leftFrame, side=TOP, expand=YES)
    finalQuery.pack(in_=rightFrame, side=TOP, expand=YES)
    finalResult.pack(in_=rightFrame, side=TOP, expand=YES)
    finalHistogram.pack(in_=rightFrame, side=TOP, expand=YES)
    window2.mainloop()