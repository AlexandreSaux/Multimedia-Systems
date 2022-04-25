def createSearchResults(myData):
    # Iterate over every results and concatenate them to mySearchResults string

    index = 1
    mySearchResults = "============================\n       Search Results       \n============================\n"
    for myElement in myData['titles']:
        if (index < 11):
            mySearchResults = mySearchResults + "-----(" + str(index) + ")-----\n"
            mySearchResults = mySearchResults + "Title: " + myElement + "\n"
            mySearchResults = mySearchResults + "Snippet: " + myData['snippets'][index - 1] + "\n\n"
            index = index + 1
    return mySearchResults