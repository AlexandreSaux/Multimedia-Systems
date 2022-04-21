from MergedPart.myLaunch import myLaunch
from MergedPart.myGlobalInit import myGlobalInit

def main():
    # Setup all the global variables and initialize them, then launch application

    myGlobalInit()
    myLaunch()
    exit(0)

if (__name__ == "__main__"):
    main()

    
