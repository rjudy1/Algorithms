# Author: Rachael Judy
# HW 6: Palindrome 15-2 Problem Implementation Based on LCS
# Usage: python Palindrome.py <string>
# Date: 10/1/2020
# Solution: The program uses the LCS of the split string to find the longest possible
#               palindrome in the string. It iterates through the possible splits of the
#               string, reverses the back string, and looks for common subsequences,
#               keeping the longest. It accounts for the odd letter that might be able to be
#               inserted into the combined subsequence and its reverse. The running time of
#               the algorithm is Theta(n^3) because LCS is Theta(n^2) and you have to
#               consider the different splits.
#

import sys


# generate the LCS and tracing tables
def Generate_Tables(x, y):
    m = len(x)
    n = len(y)

    # c table hold optimal max LCS, b table holds path along c table to get max LCS
    b = [[0 for j in range(n)] for i in range(m)]
    c = [[0 for j in range(n)] for i in range(m)]

    # iterate through, populating table
    for i in range(1, m):
        for j in range(1, n):
            # if on same letter, put a star
            if x[i] == y[j]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = "*"  # should be pointed upper left

            # if above spot is greater than left spot, follow that path
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = "^"
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = "<"
    return c, b


# interpret the tables, displaying the LCS
def Print_LCS(b, X, i, j):
    global result
    if i == 0 or j == 0:
        return

    # if on a common letter, print it backwards, else follow the arrows
    if b[i][j] == "*":
        Print_LCS(b, X, i-1, j-1)
#        print(X[i], end='')
        result += X[i]
    elif b[i][j] == "^":
        Print_LCS(b, X, i-1, j)
    else:
        Print_LCS(b, X, i, j-1)


result = "a"  # working LCS
string = ""  # initial string
longest = ""  # longest LCS

# collect from command line or default to helloworld
if len(sys.argv) == 2 and len(sys.argv[1]) != 0:
    string = sys.argv[1]
else:
    string = "helloworld"  # lowol

# get working result, keep longest
if len(string) == 1:
    longest = string
for x in range(1, int(len(string))):
    result = ""  # reset string

    # split front and back
    backSplit = string[x:]
    backSplit = backSplit[::-1]
    frontSplit = string[:x]

    # add don't care to front for one indexing purposes
    c, b = Generate_Tables("X" + backSplit, "X" + frontSplit)
    Print_LCS(b, "X" + backSplit, len(backSplit), len(frontSplit))

    # if common sequence, put together the common substring with the middle char if one exists
    if len(result) != 0:
        # check if the letters were together that were found for the palindrome, considering odd number or even together
        if result[-1] != frontSplit[-1] or result[-1] != backSplit[-1]\
                or len(backSplit) > 2 and backSplit[-1] == backSplit[-2] and result[-1] == backSplit[-1]:
            result = result + backSplit[-1] + result[::-1]

        else:
            result = result + result[::-1]

    # if no common sequence, set result to front back
    else:
        result = frontSplit[-1]

    # keep longest result
    if len(result) > len(longest):
        longest = result

# display
print("Result is: ", end=' ')
print(longest)
