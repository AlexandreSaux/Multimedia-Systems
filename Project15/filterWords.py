from nltk.corpus import stopwords

def filterWords(word):
    # Filter out stop-listed words and non-alpha tokens.

    if len(word) < 3 or word in list(stopwords.words('english')) or not word.isalpha():
        return False
    else:
        return True