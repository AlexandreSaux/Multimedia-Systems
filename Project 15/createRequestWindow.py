import tkinter as tk
from tkinter import *
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.myEndRefinement import myEndRefinement
from MergedPart.myQueryRefinement import myQueryRefinement
from MergedPart.mySearchReordering import mySearchReordering

def createRequestWindow(mySearchResults, myHistogram, window, freqs, myData):
    # Setup the window panel

    if (myGlobalInit.refinementCount == 1):
        myGlobalInit.initialQuery = myGlobalInit.myQuery
        myGlobalInit.initialResult = mySearchResults
        myGlobalInit.initialHistogram = myHistogram
    leftFrame = Frame(window)
    rightFrame = Frame(window)
    leftFrame.pack(side=LEFT)
    rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
    button1 = tk.Button(text="Search Result Reordering", width=25, height=1, command=lambda: mySearchReordering(window, freqs, myData))
    button2 = tk.Button(text="Query Refinement", width=25, height=1, command=lambda: myQueryRefinement(window, freqs, myData))
    button3 = tk.Button(text="End Refinement", width=25, height=1, command=lambda: myEndRefinement(window, mySearchResults, myHistogram))
    label1 = tk.Label(text="Your Query: " + myGlobalInit.myQuery)
    label2 = tk.Label(text=mySearchResults)
    label3 = tk.Label(text=myHistogram, justify=LEFT)
    label1.pack(in_=leftFrame, side=TOP, expand=YES)
    label2.pack(in_=leftFrame, side=TOP, expand=YES)
    label3.pack(in_=leftFrame, side=TOP, expand=YES)
    button1.pack(in_=rightFrame, side=TOP, expand=YES)
    button2.pack(in_=rightFrame, side=TOP, expand=YES)
    button3.pack(in_=rightFrame, side=TOP, expand=YES)