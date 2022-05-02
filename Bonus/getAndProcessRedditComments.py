import praw
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import threading
from bs4 import BeautifulSoup
import requests
from praw.models import MoreComments
import time
import random
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


def get_reddit_results(query):

    # The target subreddits to retrieve posts from.
    subreddits = ["reddit.com",
                  "reddit.com/r/REDDITORSINRECOVERY/",
                  "reddit.com/r/OpiatesRecovery/",
                  "reddit.com/r/opiates/",
                  "reddit.com/r/addiction/",
                  "reddit.com/r/recovery/"]

    headers = {
        'User-agent': 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36"
    }

    if len(query) == 0:
        return

    urls = []

    for sub in subreddits:
        full_query = query + " site:" + sub
        #print(full_query)

        html = requests.get(f'https://www.google.com/search?q={full_query}', headers=headers)

        soup = BeautifulSoup(html.text, 'lxml')

        for result in soup.select('.tF2Cxc'):                           
            link = result.select_one('.yuRUbf a')['href']
        
            urls.append(link)
            #print(link)
    
    return urls




def process_reddit_posts(urls, reddit):
    
    ps = PorterStemmer()
    lm = WordNetLemmatizer()

    res = []

    for url in urls:
        try:
            tok = url.split("/")
            reddit_id = tok[tok.index("comments") + 1]
            print("Reading content: " + reddit_id, end='\r')
            submission = reddit.submission(id=reddit_id)
            
            res += submission.selftext.split()
            
        except Exception as e:
            pass
            print(e)

    raw_tokens = res

    lower_tokens = [word.lower() for word in raw_tokens]

    stemmed_tokens = [] 

    for token in lower_tokens:
        stemmed_tokens.append( lm.lemmatize(token) )

    def filter_words(word):
        if len(word) < 3 or word in list(stopwords.words('english')) or not word.isalnum():         
            return False
        else:
            return True

    stop_listed_tokens = list( filter(filter_words, stemmed_tokens) )

    alt_senses = []

    for token in stop_listed_tokens:
        senses = []#wn.synsets(token)

        if (len(senses) > 0):
            for sense in senses:

                word = sense.name().split(".")[0]

                if not word == token and len(word) > 3:
                    alt_senses.append(word)
        else:
            alt_senses.append(token)

    return alt_senses

def print_histogram(term_freqs, num_freqs, max_symbs):      
    max_freq = term_freqs[0][1]
    print("============================")
    print("Top " + str(num_freqs) + " Most Frequent Term Senses")
    print("============================")

    for term in term_freqs:
        index = term_freqs.index(term)

        print("#" + str(index + 1) + " ", end="")

        for x in range(1, int( (term_freqs[index][1] / max_freq) * max_symbs) ):
            print("*", end="")

        print(" " + term_freqs[index][0] + " (" + str(term_freqs[index][1]) + ")")

    print()

