from Project15.lemmaCounter import lemmaCounter

def myReordering(freqs, myData, userInput):
    # Reordering of all search results

    titles = []
    snippets = []
    myData['items'].sort(key=lambda x: lemmaCounter(x['title'], x['snippet'], freqs[userInput - 1][0]), reverse=True)
    for item in myData['items']:
        titles.append(item['title'])
        snippets.append(item['snippet'])
    return { 'items': myData['items'], 'titles': titles, 'snippets': snippets, 'tokens': myData['tokens'] }