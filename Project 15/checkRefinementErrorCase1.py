import tkinter as tk
from tkinter import *
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.destroyWindow import destroyWindow

def checkRefinementErrorCase1(window):
    # Check if user input is a number

    userInput = 0
    try:
        userInput = int(myGlobalInit.myRefinement)
        return { 'status': TRUE, 'userInput': userInput }
    except:
        window3 = tk.Toplevel(window)
        window3.geometry("750x270")
        window3.title("Error not a number")
        label2 = tk.Label(window3, text="Error: Not a number")
        button2 = tk.Button(
            window3,
            text="Ok",
            width=25,
            height=1,
            command=lambda: destroyWindow(window3)
        )
        label2.pack(side=TOP, expand=YES)
        button2.pack(side=TOP, expand=YES)
        window3.mainloop()
        return { 'status': FALSE, 'userInput': userInput }