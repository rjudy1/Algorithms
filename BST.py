# Author: Rachael Judy
# HW 6 Q3: BST Implementation from pseudocode
# Date: 10/3/2020
#
"""
Results Printed:

Table E
[0, 0, 0, 0, 0, 0]
[0.05, 0.45000000000000007, 0.9, 1.25, 1.75, 2.75]
[0, 0.1, 0.4, 0.7, 1.2, 2.0]
[0, 0, 0.05, 0.25, 0.6, 1.2999999999999998]
[0, 0, 0, 0.05, 0.30000000000000004, 0.9]
[0, 0, 0, 0, 0.05, 0.5]
[0, 0, 0, 0, 0, 0.1]

Table W
[0, 0, 0, 0, 0, 0]
[0.05, 0.30000000000000004, 0.45, 0.55, 0.7000000000000001, 1.0000000000000002]
[0, 0.1, 0.25, 0.35, 0.49999999999999994, 0.7999999999999999]
[0, 0, 0.05, 0.15000000000000002, 0.3, 0.6]
[0, 0, 0, 0.05, 0.2, 0.5]
[0, 0, 0, 0, 0.05, 0.35]
[0, 0, 0, 0, 0, 0.1]

Table Root
[0, 0, 0, 0, 0, 0]
[0, 1, 1, 2, 2, 2]
[0, 0, 2, 2, 2, 4]
[0, 0, 0, 3, 4, 5]
[0, 0, 0, 0, 4, 5]
[0, 0, 0, 0, 0, 5]

"""


def Opt_BST(p, q, n):
    # expected cost, search cost of this subtree, root contains key index of root for [i,j]
    e = [[0 for i in range(n)] for i in range(n+1)]
    w = [[0 for i in range(n)] for i in range(n+1)]
    root = [[0 for i in range(n)] for i in range(n)]

    # initialize cost tables with the dummy probabilities
    for i in range(1, n+1):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    # fill in tables, smallest to largest, subtrees
    for l in range(1, n):
        for i in range(1, n-l+1):
            j = i + l - 1
            e[i][j] = 10000000
            w[i][j] = w[i][j-1] + p[j] + q[j]

            # try each possible index for best of subtrees
            for r in range(i, j+1):
                t = e[i][r-1] + e[r+1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r

    # return the three tables for display
    return e, w, root


# initialize probabilities and build tables
p = [  0, .15,  .1, .05,  .1, .2]
q = [.05,  .1, .05, .05, .05, .1]
e, w, root = Opt_BST(p, q, len(p))

# display the returned tables
print("Table E")
for x in e:
    print(x)
print()

print("Table W")
for x in w:
    print(x)
print()

print("Table Root")
for x in root:
    print(x)
print() # results