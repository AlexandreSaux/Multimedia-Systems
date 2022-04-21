import JustinPart.myConfig as myConfig

def get_results(query, num_results):
    position = 1        # Current search result (default to 1).

    titles = []         # To hold data.
    snippets = []
    links = []
    all_items = []

    for num in range(1, num_results):     # Retrieves search results in batches of 10, based on NUM_RESULTS. 
        position += 10

        search_results = myConfig.service.cse().list(q=query, cx=myConfig.SEARCH_ENGINE_ID, start=position).execute()


        query_info = search_results['queries']
        items = search_results['items']

        all_items += items
        


        for item in items:                          # Get specific metadata from search result.
            titles.append(item['title'])
            snippets.append(item['snippet'])
            links.append(item['link'])

    return { 'items': all_items, 'titles': titles, 'snippets': snippets, 'links': links }