from collections import Counter
from Project15.filterWords import filterWords
import Project15.myGlobalInit as myGlobalInit

def createHistogram(myData):
    # Use token system to build word frequency table and then concatenate it to myHistogram string

    stemmed_tokens = [] 
    myHistogram = "============================\n Top " + str(myGlobalInit.NUM_FREQS) + " Most Frequent Terms \n============================\n"
    lower_tokens = [word.lower() for word in myData['tokens']]
    for token in lower_tokens:
        stemmed_tokens.append(myGlobalInit.lm.lemmatize(token))    
    tokens = list(filter(filterWords, stemmed_tokens))
    freqs = Counter(tokens).most_common(myGlobalInit.NUM_FREQS)
    for term in freqs:
        max_freq = freqs[0][1]
        index = freqs.index(term)
        if ((index + 1) >= 10):
            myHistogram = myHistogram + "#" + str(index + 1) + " "
        else:
            myHistogram = myHistogram + "#" + str(index + 1) + "  "
        for x in range(1, int( (freqs[index][1] / max_freq) * myGlobalInit.MAX_SYMBS) ):
            myHistogram = myHistogram + "*"
        myHistogram = myHistogram + " " + freqs[index][0] + " (" + str(freqs[index][1]) + ")\n"
    return { 'histogram': myHistogram, 'freqs': freqs }