from tkinter import *
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.checkRefinementErrorCase1 import checkRefinementErrorCase1
from MergedPart.checkRefinementErrorCase2 import checkRefinementErrorCase2

def myRefinementErrorCheck(entry, window2, senses):
    # Launch the two error case function

    myGlobalInit.myRefinement = entry.get()
    myCheck = checkRefinementErrorCase1(window2)
    userInput = myCheck['userInput']
    if (myCheck['status'] == FALSE):
        return
    if (checkRefinementErrorCase2(window2, userInput, len(senses)) == FALSE):
        return
    window2.destroy()
    myGlobalInit.myQuery = myGlobalInit.myQuery + " " + senses[int(myGlobalInit.myRefinement) - 1].name().split(".")[0]