#import JustinPart.myConfig as myConfig
import praw
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import threading
from bs4 import BeautifulSoup
import requests
from praw.models import MoreComments


def myRequest():
    query = input("Enter a query: ") + " site:reddit.com"
    data = []
    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36"
    }
    html = requests.get(f'https://www.google.com/search?q={query}', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    for result in soup.select('.tF2Cxc'):
        title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
        displayed_link = result.select_one('.TbwUpd.NJjxre').text
        try:
            snippet = result.select_one('#rso .lyLwlc').text
        except:
            snippet = None
        print(f'{title}\n{link}\n{displayed_link}\n{snippet}\n')
        data.append(link)

    return data

lm = WordNetLemmatizer()

reddit = praw.Reddit(
                     client_id="wOxGKQeSHfDjQVP606-3LA",
                     client_secret="elC3Aa64_jAnsarkHfs83su87fK_SQ",
                     user_agent="Windows:RedditCommentRetriever:v1 (by u/JY2000)"
                    )



def get_and_process_reddit_comments(urls):

    res = []


    for url in urls:
        try:
            tok = url.split("/")
            reddit_id = tok[tok.index("comments") + 1]
            print(reddit_id)
            submission = reddit.submission(id=reddit_id)
            
            res += submission.comments.list()
        except:
            print("invalid link")

    raw_tokens = []

    print(str(len(res)) + " comments retrieved.")

    for comment in res:
        if isinstance(comment, MoreComments):
            continue
        raw_tokens += comment.body.split()

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

    return stop_listed_tokens

def print_histogram(term_freqs, num_freqs, max_symbs):      
    max_freq = term_freqs[0][1]
    print("============================")
    print("Top " + str(num_freqs) + " Most Frequent Terms")
    print("============================")

    for term in term_freqs:
        index = term_freqs.index(term)

        print("#" + str(index + 1) + " ", end="")

        for x in range(1, int( (term_freqs[index][1] / max_freq) * max_symbs) ):
            print("*", end="")

        print(" " + term_freqs[index][0] + " (" + str(term_freqs[index][1]) + ")")

    print()

print_histogram( Counter( get_and_process_reddit_comments( myRequest() ) ).most_common(100), 100, 50 )
