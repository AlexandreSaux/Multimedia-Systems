def print_results(query, data, max):
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