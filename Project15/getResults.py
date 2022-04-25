import time
import random
import requests
from bs4 import BeautifulSoup
import Project15.myGlobalInit as myGlobalInit

def getResults():
    # Initialize every value

    position = 1
    titles = []
    snippets = []
    all_items = []
    raw_tokens = []
    headers = {
        'User-agent': 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.50"
    }
    # Retrieves search results in batches of 10, based on NUM_RESULTS. 

    for x in range(0, myGlobalInit.NUM_RESULTS):
        #print("Getting results... (" + str( round( (x / myGlobalInit.NUM_RESULTS) * 100) ) + "%)", end='\r')
        html = requests.get(f'https://www.google.com/search?q={myGlobalInit.myQuery}&start={position}', headers=headers)
        pause_time = random.randint(8, 15) / 10
        time.sleep( pause_time )
        # Correction of time taking into account pausing.

        myGlobalInit.TIME_ADJUSTMENT -= pause_time
        soup = BeautifulSoup(html.text, 'lxml')
        # Get specific metadata from search result.

        for result in soup.select('.tF2Cxc'):
            title = result.select_one('.DKV0Md').text
            link = result.select_one('.yuRUbf a')['href']
            try:
                snippet = result.select_one('#rso .lyLwlc').text
            except:
                snippet = ""
            all_items.append({'title': title, 'snippet': snippet, 'link': link})
            titles.append(title)
            raw_tokens += title.split()
            snippets.append(snippet)
            raw_tokens += snippet.split()
        position += 10
    return { 'items': all_items, 'titles': titles, 'snippets': snippets, 'tokens': raw_tokens }