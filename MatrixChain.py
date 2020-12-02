# Author: Rachael Judy
# HW 5: 15.2-1 with matrix chain <5, 10, 6, 9, 4, 20, 6, 12, 8>
# Implementation based on one indexed pseudocode
#
#
#
"""
Results:
(((A1A2)(A3A4))(((A5A6)A7)A8)) = ( ( ((5x10)(10x6)) ((6x9)(9x4)) ) (( ((4x20)(20x6)) (6x12)) (12x8)) )
Optimal solution is m[1,8] = 1948 multiplications

Note - zeros at index zero for both column and row are necessary due to the 1 indexing

M Table
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 300, 570, 636, 1036, 1236, 1596, 1948]
[0, 0, 0, 540, 456, 1256, 1176, 1704, 1928]
[0, 0, 0, 0, 216, 696, 840, 1272, 1560]
[0, 0, 0, 0, 0, 720, 696, 1200, 1440]
[0, 0, 0, 0, 0, 0, 480, 768, 1152]
[0, 0, 0, 0, 0, 0, 0, 1440, 1536]
[0, 0, 0, 0, 0, 0, 0, 0, 576]
[0, 0, 0, 0, 0, 0, 0, 0, 0]

S Table
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 1, 2, 2, 4, 4, 6, 4]
[0, 0, 0, 2, 2, 4, 4, 4, 4]
[0, 0, 0, 0, 3, 4, 4, 4, 4]
[0, 0, 0, 0, 0, 4, 4, 4, 4]
[0, 0, 0, 0, 0, 0, 5, 6, 7]
[0, 0, 0, 0, 0, 0, 0, 6, 6]
[0, 0, 0, 0, 0, 0, 0, 0, 7]
[0, 0, 0, 0, 0, 0, 0, 0, 0]

"""


# do one indexing, generate tables cost and solution tables
def Matrix_Chain_Order(p):
    n = len(p)

    # minimum cost table and solution
    m = [[0 for j in range(n)] for i in range(n)]
    s = [[0 for j in range(n)] for i in range(n)]

    # populate tables
    for l in range(2, n):
        for i in range(1, n - l + 1):
            j = i + l - 1

            # set current cost very high
            m[i][j] = 1000000
            for k in range(i, j):
                # calculate cost, increasing chain length, finding splits
                q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]

                # keep lowest cost/position stored
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k
    return m, s


# display results of tables
def Print_Optimal_Parens(s, i, j):
    if i == j:
        print("A"+str(i), end='')
    else:
        print("(", end='')
        Print_Optimal_Parens(s, i, s[i][j])
        Print_Optimal_Parens(s, s[i][j] + 1, j)
        print(")", end='')

# display tables
p = [5, 10, 6, 9, 4, 20, 6, 12, 8]
m, s = Matrix_Chain_Order(p)
print("M Table")
for i in m:
    print(i)
print()

print("S Table")
for j in s:
    print(j)
print()

# display results
Print_Optimal_Parens(s, 1, 8)