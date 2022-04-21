from tkinter import *
import MergedPart.myRequest as myRequest
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.myReordering import myReordering
from MergedPart.checkErrorCase1 import checkErrorCase1
from MergedPart.checkErrorCase2 import checkErrorCase2

def mySetValueReordering(entry, window, window2, freqs, myData):
    # Error check for the user input

    myGlobalInit.myReordering = entry.get()
    window2.destroy()
    myCheck = checkErrorCase1(window)
    userInput = myCheck['userInput']
    if (myCheck['status'] == FALSE):
        return
    if (checkErrorCase2(window, userInput) == FALSE):
        return
    window.destroy()

    # Launch the reordering and save it
    myGlobalInit.myData = myReordering(freqs, myData, userInput)
    myRequest.myRequest()