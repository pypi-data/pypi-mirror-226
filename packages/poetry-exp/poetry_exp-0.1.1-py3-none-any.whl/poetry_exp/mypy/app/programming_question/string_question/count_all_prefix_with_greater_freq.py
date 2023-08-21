"""
Count all prefixes in given string with greatest frequency
Given a string, print and count all prefixes in which first alphabet has greater frequency than second alphabet.

Take two alphabets from the user and compare them. The prefixes in which the alphabet given first has greater frequency than the second alphabet, such prefixes are printed, else the result will be 0.

Examples :

Input : string1 = "geek",
        alphabet1 = "e", alphabet2 = "k"
Output :
ge
gee
geek
3

Input : string1 = "geek",
        alphabet1 = "k", alphabet2 = "e"
Output :
0
"""



# Python program to Count all
# prefixes in given string with
# greatest frequency

# Function to print the prefixes
def prefix(string1, alphabet1, alphabet2):
    count = 0
    non_empty_string = ""

    string2 = list(string1)

    # Loop for iterating the length of
    # the string and print the prefixes
    # and the count of query prefixes.
    for i in range(0, len(string2)):
        non_empty_string = non_empty_string + (string2[i])

        if (non_empty_string.count(alphabet1) >
                non_empty_string.count(alphabet2)):
            # prints all required prefixes
            print(non_empty_string)

            # increment count
            count += 1

    # returns count of the
    # required prefixes
    return (count)


# Driver Code
print(prefix("geeksforgeeks", "e", "g"))
