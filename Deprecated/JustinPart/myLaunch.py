from JustinPart.getResults import get_results
from JustinPart.processResult import process_results
from JustinPart.generateFreqs import generate_freqs
from JustinPart.printResults import print_results
from JustinPart.printHistogram import print_histogram
from JustinPart.reorder import reorder
import JustinPart.myConfig as myConfig
import nltk
from nltk.corpus import wordnet as wn

def myLaunch():
    user_input = ""

    refinement_state = False        # True if user is performing query refinement or search result reordering.
    sorting_state = False
    print("*Type 'QUIT' to exit the program.*\n")

    while (not user_input == "QUIT"):
        if not refinement_state and not sorting_state:
            user_input = input("Enter a query: ")
        
        query = user_input

        if (user_input == "QUIT"):
            return

        if not sorting_state:
            data = get_results(user_input, int( (myConfig.NUM_RESULTS / 10) + 1) )         # Ten results per count retrieved, divide by 10 to get actual amount.
            print("data:" + str(len(data['items'])))
            tokens = process_results(data)
            freqs = generate_freqs(tokens, myConfig.NUM_FREQS)

        print_results(user_input, data, myConfig.MAX_PRINT)


        print_histogram(freqs, myConfig.NUM_FREQS, myConfig.MAX_SYMBS)






        
        
        if not sorting_state:
            user_input = int( input("Make a selection: \n\
                                [1] Search Result Reordering \n\
                                [2] Query Refinement\n\
                                [3] Return\n\n") )
        else:
            user_input = 1

        if user_input == 1:
            sorting_state = True
            user_input = int( input("Enter a target term to sort results by: ") )

            print( str(user_input) )
            
            if (user_input > myConfig.NUM_FREQS or user_input <= 0):
                print("Invalid selection made. Aborting.\n")
                sorting_state = False
                continue


            data = reorder(data, freqs[user_input - 1][0])
            user_input = str(query)


        elif user_input == 2:
            user_input = int( input("Enter a term number to expand: ") )

            if (user_input > myConfig.NUM_FREQS or user_input <= 0):
                print("Invalid selection made. Aborting.\n")
                continue

            term = freqs[user_input - 1][0]
            senses = wn.synsets(term)

            if (len(senses) > 0):

                index = 0

                print("============================")
                print("Alternative Senses For Term \"" + term + "\"")
                print("============================")

                for sense in senses:
                    print("#" + str(index + 1) + " " + sense.name() + ": " + sense.definition())
                    index += 1

                print()
                user_input = int(input("Select a sense of the term: "))

                if (user_input > len(senses) or user_input <= 0):
                    print("Invalid selection made. Aborting.\n")
                    continue
                else:
                    user_input = str(query) + " " + senses[user_input - 1].name().split(".")[0]
                    refinement_state = True
                
            else:
                print("No alternative senses found for term \"" + term + "\"\n")
                user_input = str(query) + " " + term
                refinement_state = True

        else:
            print("Returning to query formulation.")
            refinement_state = False
            sorting_state = False