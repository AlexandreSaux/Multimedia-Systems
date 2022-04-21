import tkinter as tk
from tkinter import *
from MergedPart.getResults import getResults
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.myWindowInit import myWindowInit
from MergedPart.createHistogram import createHistogram
from MergedPart.createSearchResults import createSearchResults
from MergedPart.createRequestWindow import createRequestWindow

def myRequest():
    # Initialize variables
    
    window = tk.Tk()
    myGlobalInit.refinementCount += 1
    # Initialize window elements, create myData object and use it to create myHistogram and mySearchResults strings

    myWindowInit(window)
    if (myGlobalInit.refinementCount == 1 or myGlobalInit.isRefined):
        myData = getResults()
    else:
        myData = myGlobalInit.myData
    myData2 = createHistogram(myData)
    myHistogram = myData2['histogram']
    mySearchResults = createSearchResults(myData)
    # Then use those strings to setup the window and finally open window loop

    createRequestWindow(mySearchResults, myHistogram, window, myData2['freqs'], myData)
    window.mainloop()









