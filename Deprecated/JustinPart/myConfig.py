import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from googleapiclient.discovery import build

def myInit():
    global NUM_RESULTS
    global NUM_FREQS
    global MAX_SYMBS
    global MAX_PRINT
    global ps
    global lm
    global SEARCH_TYPE
    global VERSION
    global API_KEY
    global SEARCH_ENGINE_ID
    global service

    # Constants
    NUM_RESULTS = 20            # Number of results to retrieve (must be multiple of 10).
    NUM_FREQS = 20              # Number of most frequent terms to calculate to.
    MAX_SYMBS = 60              # Width of the printed rudimentary histogram in characters.
    MAX_PRINT = 10              # Max search results to display at a time.
    ps = PorterStemmer()
    lm = WordNetLemmatizer()
    SEARCH_TYPE = "customsearch"
    VERSION = "v1"
    API_KEY = "AIzaSyCsz2kG8FnqX_ehWEQimvreksyBRWL1eNg"
    SEARCH_ENGINE_ID = 'b360fd3ec1b70b6b8'
    service = build(SEARCH_TYPE, VERSION, developerKey=API_KEY)
    nltk.download('wordnet')
    nltk.download('stopwords')