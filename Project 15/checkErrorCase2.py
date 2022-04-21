import tkinter as tk
from tkinter import *
import MergedPart.myGlobalInit as myGlobalInit
from MergedPart.destroyWindow import destroyWindow

def checkErrorCase2(window, userInput):
    # Check if user input is correct

    if (userInput > myGlobalInit.NUM_FREQS or userInput <= 0):
        window4 = tk.Toplevel(window)
        window4.geometry("750x270")
        window4.title("Error: Not between 0 and " + str(myGlobalInit.NUM_FREQS))
        label2 = tk.Label(window4, text="Error: Not between 1 and " + str(myGlobalInit.NUM_FREQS))
        button2 = tk.Button(
            window4,
            text="Ok",
            width=25,
            height=1,
            command=lambda: destroyWindow(window4)
        )
        label2.pack(side=TOP, expand=YES)
        button2.pack(side=TOP, expand=YES)
        window4.mainloop()
        return FALSE