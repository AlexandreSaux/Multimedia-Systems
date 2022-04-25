from tkinter import *
from nltk.corpus import wordnet as wn
import Project15.myGlobalInit as myGlobalInit
from Project15.myRefinementFirstCase import myRefinementFirstCase
from Project15.myRefinementSecondCase import myRefinementSecondCase

def myRefinement(freqs, window, userInput):
    # Launch the two case function

    term = freqs[userInput - 1][0]
    senses = wn.synsets(term)
    if (len(senses) > 0):
        myRefinementFirstCase(term, senses)
    else:
        myRefinementSecondCase(term, window)
    myGlobalInit.isRefined = TRUE