import JustinPart.myConfig as myConfig

def reorder(results, term):

    def lemma_counter(title, snippet):
        count = 0

        lemmatized = []

        for x in title.lower().split():
            lemmatized.append( myConfig.lm.lemmatize(x) )

        for x in snippet.lower().split():
            lemmatized.append( myConfig.lm.lemmatize(x) )

        return lemmatized.count(term)


    results['items'].sort(key=lambda x: lemma_counter(x['title'], x['snippet']), reverse=True)

    titles = []         # To hold data.
    snippets = []
    links = []

    for item in results['items']:                          # Get specific metadata from search result.
        titles.append(item['title'])
        snippets.append(item['snippet'])
        links.append(item['link'])

    return { 'items': results['items'], 'titles': titles, 'snippets': snippets, 'links': links }