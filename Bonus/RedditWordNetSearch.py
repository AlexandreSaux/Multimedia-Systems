import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
import time
import webbrowser
import enum
from bs4 import BeautifulSoup
import requests
import random
import os
import getAndProcessRedditComments as rd
#nltk.download('omw-1.4')

ps = PorterStemmer()
lm = WordNetLemmatizer()

##################################
# Data retrieval and processing
##################################

def get_results(query, num_results):

    if len(query) == 0:
        return

    headers = {
        'User-agent': 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36"
    }

    position = 1        # Current search result (default to 1).

    titles = []         # To hold data.
    snippets = []
    links = []
    all_items = []

    for x in range(0, num_results):         # Retrieves search results in batches of 10, based on NUM_RESULTS. 

        print("Getting results... (" + str( round( (x / num_results) * 100) ) + "%)", end='\r')

        html = requests.get(f'https://www.google.com/search?q={query}&start={position}', headers=headers)

        pause_time = random.randint(8, 15) / 10
        time.sleep( pause_time )

        soup = BeautifulSoup(html.text, 'lxml')

        for result in soup.select('.tF2Cxc'):                           # Get specific metadata from search result.
            title = result.select_one('.DKV0Md').text
            link = result.select_one('.yuRUbf a')['href']
            displayed_link = result.select_one('.TbwUpd.NJjxre').text
            try:
                snippet = result.select_one('#rso .lyLwlc').text
            except:
                snippet = ""

            all_items.append({'title': title, 'snippet': snippet, 'link': link})
            titles.append(title)
            snippets.append(snippet)
            links.append(link)

        position += 10

    return { 'items': all_items, 'titles': titles, 'snippets': snippets, 'links': links }
   

def process_results(query):
    import praw
    reddit = praw.Reddit(
                         client_id="wOxGKQeSHfDjQVP606-3LA",
                         client_secret="elC3Aa64_jAnsarkHfs83su87fK_SQ",
                         user_agent="Windows:RedditCommentRetriever:v1 (by u/JY2000)"
                        )

    return rd.process_reddit_posts( rd.get_reddit_results(query), reddit )


def generate_freqs(tokens, num):
    return Counter(tokens).most_common(num)

def generate_sense_freqs(freqs, num):
    senses = []

    for term in freqs:
        addition = []

        for sense in wn.synsets(term[0]):

            curr = sense.name().split(".")[0]
            if addition.count(curr) == 0:
                addition.append(curr)

        senses += addition   

    senses_ranked = generate_freqs(senses, num)

    return senses_ranked

##################################
# Information Display
##################################

def print_results(query, data, max):
    if data == None:
        return

    print("============================")           # Display information to the user.
    print("Search Results")
    print("============================")

    for x in range(1, max + 1):
        print("-----(" + str(x) + ")-----")
        print("Title: " + data['titles'][x - 1])
        print("Snippet: " + data['snippets'][x - 1])
        print("Link: " + data['links'][x - 1])
        print()

    print("***showing " + str(max) + " of " + str( len(data['titles']) ) + " results for \"" + str(query) + "\"***")
    print()

def print_histogram(term_freqs, sense_freqs, num_freqs, max_symbs):        # Prints histogram for top "num_top" most frequent terms, with a width of "max_symbs" characters.
    if len(term_freqs) == 0:
        return 

    max_freq = term_freqs[0][1]
    print("=========================================")
    print("Top " + str(num_freqs) + " Most Frequent Terms From Reddit")
    print("=========================================")

    for term in term_freqs:
        index = term_freqs.index(term)

        print("#" + str(index + 1) + " ", end="")

        for x in range(1, int( (term_freqs[index][1] / max_freq) * max_symbs) ):
            print("*", end="")

        print(" " + term_freqs[index][0] + " (" + str(term_freqs[index][1]) + ")")

    print()

    max_freq = sense_freqs[0][1]
    print("=========================================")
    print("Top " + str(num_freqs) + " Senses Expanded From Terms")
    print("=========================================")

    for sense in sense_freqs:
        index = sense_freqs.index(sense)

        print("#" + str(index + 1) + " ", end="")

        for x in range(1, int( (sense_freqs[index][1] / max_freq) * max_symbs) ):
            print("*", end="")

        print(" " + sense_freqs[index][0] + " (" + str(sense_freqs[index][1]) + ")")

################################################################
# Query expansion using WordNet and search result reordering
################################################################

def reorder(results, term):

    def lemma_counter(title, snippet):
        count = 0

        lemmatized = []

        for x in title.lower().split():
            lemmatized.append( lm.lemmatize(x) )

        for x in snippet.lower().split():
            lemmatized.append( lm.lemmatize(x) )

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

################################
# Bookkeeping and Evalution
################################

actions = 0                 # The number of actions taken in the CLI (equivalent to number of clicks in a GUI).

start_time = time.time()
time_elapsed = None         # The total time taken to complete the task. Evaluated after program is exited.

def save_data(end_time):
    global time_elapsed
    time_elapsed = round(end_time - start_time + TIME_ADJUSTMENT, 2) 

    file = open("WordBarsEvaluation.txt", "a+")

    file.writelines(["\nACTIONS=" + str(actions), "\nTIME=" + str(time_elapsed)])
    file.close()

    print("\n===================")
    print("Overview")
    print("===================")

    print("Actions Taken: " + str(actions))
    print("Time Taken: " + str(time_elapsed) + " seconds\n")
    print("Data has been saved.")

#####################
# Parameters
#####################

NUM_RESULTS = 100            # Number of results to retrieve (must be multiple of 10).
NUM_FREQS = 20              # Number of most frequent terms to calculate to.
MAX_SYMBS = 60              # Width of the printed rudimentary histogram in characters.
MAX_PRINT = 10              # Max search results to display at a time.
EXIT_STRING = "0"           # When entered as the query, exits the program.
TIME_ADJUSTMENT = 0         # Adjust evaluation time for pausing due to speed limits.

#############################
# Main Method and Functions
#############################

clear = lambda: os.system('cls')

def open_link(data):
    global actions
    user_input = -1

    while (user_input != 0 and user_input <= len(data['links'])):
        try:
            user_input = int( input("Select a link number to open ('0' to return): ") )
        except:
            user_input = 0
        

        if user_input == 0:
            break

        webbrowser.open(data['links'][user_input - 1])

    print("Invalid selection made. Aborting.\n")
    return

def main():
    user_input = ""

    global actions
    data = None
    tokens = None
    freqs = None
    senses = None

    def get_process_print_results(query):                                          # Retrieves search results, processes them, gets term frequenciesm and prints information all in one function.
        nonlocal data
        nonlocal tokens
        nonlocal freqs
        nonlocal senses

        data = get_results(user_input, int( (NUM_RESULTS / 10) + 1) )         # Ten results per count retrieved, divide by 10 to get actual amount.

        clear()

        tokens = process_results(query)
        freqs = generate_freqs(tokens, NUM_FREQS)
        senses = generate_sense_freqs(freqs, NUM_FREQS)

        print_results(user_input, data, MAX_PRINT)

        print_histogram(freqs, senses, NUM_FREQS, MAX_SYMBS)

        return

    class Action(enum.Enum):
        reorder = 1
        refine = 2
        open = 3
        remove = 4
        ret = 5

    while (not user_input == EXIT_STRING):

        print("*Type \"" + EXIT_STRING + "\" to exit the program.*\n")
        user_input = input("Enter a query: ")

        query = user_input

        if (user_input == EXIT_STRING):
            return

        get_process_print_results(query)
        
        while user_input != Action.ret.value:

            if len( str(user_input) ) == 0:
                print("Nothing entered.\n")
                break

            try:
                user_input = int( input("Make a selection: \n\
                                    [1] Search Result Reordering \n\
                                    [2] Query Refinement\n\
                                    [3] Open Link\n\
                                    [4] Remove Last Term From Query\n\
                                    [5] Return\n\n") )
            except:
                user_input = 0
            

            if user_input == Action.reorder.value:
                try: 
                    selection = int( input("\nChoose a table to select from: \n\
                                            [1] Most Frequent Terms From Reddit\n\
                                            [2] Most Frequent Senses\n") )
                    if user_input == 0:
                        continue
                except:
                    user_input = 0
                    print("Invalid selection made. Returning.\n")
                    continue

                try:
                    user_input = int( input("Enter a target term to sort results by ('0' to return): ") )
                except:
                    user_input = 0

                

                while (user_input <= NUM_FREQS and user_input > 0):
                    clear()

                    if selection == 1:
                        data = reorder(data, freqs[user_input - 1][0])
                    elif selection == 2:
                        data = reorder(data, senses[user_input - 1][0])
                    else:
                        break

                    user_input = query
               
                    print_results(user_input, data, MAX_PRINT)
                    print_histogram(freqs, senses, NUM_FREQS, MAX_SYMBS)

                    try: 
                        selection = int( input("Choose a table to select from: \n\
                                            [1] Most Frequent Terms From Reddit\n\
                                            [2] Most Frequent Senses\n") )
                    except:
                        user_input = 0
                        break
                    try:
                        user_input = int( input("Enter a target term to sort results by ('0' to return): ") )
                    except:
                        user_input = 0
                

                print("Invalid selection made. Returning.\n")
                user_input = str(query)
                continue

            elif user_input ==  Action.refine.value:
                try: 
                    selection = int( input("Choose a table to select from: \n\
                                            [1] Most Frequent Terms From Reddit\n\
                                            [2] Most Frequent Senses\n") )
                except:
                    user_input = 0
                try:
                    user_input = int( input("Enter a term number to expand: ") )
                except:
                    user_input = 0

                

                if (user_input > NUM_FREQS or user_input <= 0 or selection <= 0 or selection > 2):
                    print("Invalid selection made. Returning.\n")
                    continue

                if selection == 1:
                    term = freqs[user_input - 1][0]
                elif selection == 2:
                    term = senses[user_input - 1][0]

                user_input = str(query) + " " + term

                query = user_input

                get_process_print_results(query)
        

            elif user_input ==  Action.open.value:
                open_link(data)

            elif user_input == Action.remove.value:
                if len(query.split(" ")) <= 1:
                    print("Cannot reduce query any further.\n")
                else:
                    user_input = query.rsplit(' ', 1)[0]
                    query = user_input

                print("Your query is now \"" + str(query) + "\"\n")
        
            elif user_input == Action.ret.value:
                pass
            else:
                print("Invalid selection. Try again.\n")

        print("Returning to query formulation.\n")


main()

save_data(time.time())
    


