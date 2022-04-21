import nltk
from tkinter import *
from pickle import FALSE
from nltk.stem import WordNetLemmatizer

def myGlobalInit():
    
    # Initialize every global variables and constants
    
    global lm
    global myData
    global myQuery
    global NUM_FREQS
    global MAX_SYMBS
    global isRefined
    global NUM_RESULTS
    global myRefinement
    global myReordering
    global initialQuery
    global initialResult
    global TIME_ADJUSTMENT
    global refinementCount
    global initialHistogram
    
    # Set the by default value for every single global variables and constants

    lm = WordNetLemmatizer()
    myData = { }
    myQuery = ""
    NUM_FREQS = 20
    MAX_SYMBS = 60
    isRefined = FALSE
    NUM_RESULTS = 10
    myRefinement = ""
    myReordering = ""
    initialQuery = ""
    initialResult = ""
    TIME_ADJUSTMENT = 0
    refinementCount = 0
    initialHistogram = ""

    # Download wordnet and stopwords

    nltk.download('wordnet')
    nltk.download('stopwords')
    
    