def print_histogram(term_freqs, num_freqs, max_symbs):        # Prints histogram for top "num_top" most frequent terms, with a width of "max_symbs" characters.
    max_freq = term_freqs[0][1]
    print("============================")
    print("Top " + str(num_freqs) + " Most Frequent Terms")
    print("============================")
    
    print(type(term_freqs[0]))

    for term in term_freqs:
        index = term_freqs.index(term)

        print("#" + str(index + 1) + " ", end="")

        for x in range(1, int( (term_freqs[index][1] / max_freq) * max_symbs) ):
            print("*", end="")

        print(" " + term_freqs[index][0] + " (" + str(term_freqs[index][1]) + ")")