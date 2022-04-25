from tkinter import *
import Project15.myRequest as myRequest
import Project15.myGlobalInit as myGlobalInit
from Project15.myRefinement import myRefinement
from Project15.checkErrorCase2 import checkErrorCase2
from Project15.checkRefinementErrorCase1 import checkRefinementErrorCase1


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