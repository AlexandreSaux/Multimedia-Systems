import tkinter as tk
from tkinter import *
import Project15.myGlobalInit as myGlobalInit
from Project15.destroyWindow import destroyWindow

def mySetValue(entry, window):
    # Retrieve query from UI elements and store it in global variable myQuery

    myGlobalInit.myQuery = entry.get()
    if (myGlobalInit.myQuery == ""):
        window2 = tk.Toplevel(window)
        window2.geometry("750x270")
        window2.title("Error no query")
        label2 = tk.Label(window2, text="Error: query is empty")
        button2 = tk.Button(
            window2,
            text="Ok",
            width=25,
            height=1,
            command=lambda: destroyWindow(window2)
        )
        label2.pack(side=TOP, expand=YES)
        button2.pack(side=TOP, expand=YES)
        window2.mainloop()
    else:
        window.destroy()