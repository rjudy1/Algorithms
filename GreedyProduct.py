# Author: Rachael Judy
# Date: 10/5/2020
# Code for Product

## Counting Sort ## Assumes range 1 to number_elements (global)
def CountSort(arr):
    output = [0 for i in range(50)] # output array
    countArr = [0 for i in range(50)]

    for i in arr:  # count the occurrences of each character
        countArr[i] += 1
    for i in range(1, len(countArr)):  # modify array to contain position of this character in the array
        countArr[i] += countArr[i-1]

    # create output array
    for i in range(len(arr)):
        output[countArr[arr[i]] - 1] = arr[i]   # place arr item in calculated place
        countArr[arr[i]] -= 1                   # reduce count of those by one

    # copy output over to input
    for i in range(len(arr)):
        arr[i] = output[i]


A = [3, 4, 2]
B = [4, 5, 7]
CountSort(A)
CountSort(B)

product = 1
for i in range(len(A)):
    product *= A[i]**B[i]
print(product)