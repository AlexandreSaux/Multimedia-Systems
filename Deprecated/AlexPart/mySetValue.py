import AlexPart.myConfig as myConfig

def mySetValue(entry, window):
    myConfig.myQuery = entry.get()
    window.destroy()