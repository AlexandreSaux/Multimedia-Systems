from tkinter import *
import MergedPart.myRequest as myRequest
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.myRefinement import myRefinement
from MergedPart.checkErrorCase2 import checkErrorCase2
from MergedPart.checkRefinementErrorCase1 import checkRefinementErrorCase1


def mySetValueRefinement(entry, window, window2, freqs):
    # Error check for the user input

    myGlobalInit.myRefinement = entry.get()
    window2.destroy()
    myCheck = checkRefinementErrorCase1(window)
    userInput = myCheck['userInput']
    if (myCheck['status'] == FALSE):
        return
    if (checkErrorCase2(window, userInput) == FALSE):
        return
    window.destroy()

    # Launch the reordering and save it
    myGlobalInit.myData = myRefinement(freqs, window, userInput)
    myRequest.myRequest()