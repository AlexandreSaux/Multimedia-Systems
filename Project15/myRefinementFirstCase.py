import tkinter as tk
from tkinter import *
from Project15.myRefinementErrorCheck import myRefinementErrorCheck

def myRefinementFirstCase(term, senses):
    # If there is alternative expand on them

    index = 0
    myRefinement = ""
    myTitle = "============================\nAlternative Senses For Term \"" + term + "\"" + "\n============================\n\n"
    for sense in senses:
        myRefinement = myRefinement + "#" + str(index + 1) + " " + sense.name() + ": " + sense.definition() + "\n"
        index += 1
    window2 = tk.Tk()
    window2.title("Multimedia Systems Project 15")
    label = tk.Label(window2, text=myTitle)
    label2 = tk.Label(window2, text=myRefinement, justify=LEFT)
    label3 = tk.Label(window2, text="Select a sense of the term")
    entry = tk.Entry(window2, width=50)
    button = tk.Button(
        window2,
        text="Submit",
        width=25,
        height=1,
        command=lambda: myRefinementErrorCheck(entry, window2, senses)
    )
    label.pack(side=TOP, expand=YES)
    label2.pack(side=TOP, expand=YES)
    label3.pack(side=TOP, expand=YES)
    entry.pack(side=TOP, expand=YES)
    button.pack(side=TOP, expand=YES)
    window2.mainloop()