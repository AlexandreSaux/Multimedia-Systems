from tkinter import *
from nltk.corpus import wordnet as wn
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.myRefinementFirstCase import myRefinementFirstCase
from MergedPart.myRefinementSecondCase import myRefinementSecondCase

def myRefinement(freqs, window, userInput):
    # Launch the two case function

    term = freqs[userInput - 1][0]
    senses = wn.synsets(term)
    if (len(senses) > 0):
        myRefinementFirstCase(term, senses)
    else:
        myRefinementSecondCase(term, window)
    myGlobalInit.isRefined = TRUE