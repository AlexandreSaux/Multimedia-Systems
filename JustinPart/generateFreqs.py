from collections import Counter

def generate_freqs(tokens, num):
    return Counter(tokens).most_common(num)