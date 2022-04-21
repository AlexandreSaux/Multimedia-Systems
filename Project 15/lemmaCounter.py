import MergedPart.myGlobalInit as myGlobalInit

def lemmaCounter(title, snippet, term):
    # Count the lemma

    lemmatized = []
    for x in title.lower().split():
        lemmatized.append(myGlobalInit.lm.lemmatize(x) )
    for x in snippet.lower().split():
        lemmatized.append(myGlobalInit.lm.lemmatize(x) )
    return lemmatized.count(term)