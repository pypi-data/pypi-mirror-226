def find_triplet(arr, sum):
    triplet_list = []
    arr_size=len(arr)
    # Fix the first element as A[i]
    for i in range(0, arr_size-2):
        # Fix the second element as A[j]
        for j in range(i+1, arr_size-1):
            # Now look for the third number
            for k in range(j+1, arr_size):
                if arr[i] + arr[j] + arr[k] == sum:
                    print "Triplet is: {0}, {1}, {2}".format(arr[i], arr[j],  arr[k])
                    triplet_list.append((arr[i], arr[j],  arr[k]))

    return triplet_list


def findTriplets(arr):
    found = False

    # sort array elements
    arr.sort()
    n = len(arr)
    for i in range(n):

        # initialize left and right
        l = i + 1
        r = n - 1
        x = arr[i] # take one element and do some from all possible elelments
        while l < r:

            if x + arr[l] + arr[r] == 0:
                # print elements if it's sum is zero
                print(x, arr[l], arr[r])
                l += 1
                r -= 1
                found = True

            # If sum of three elements is less
            # than zero then increment in left
            elif x + arr[l] + arr[r] < 0:
                l += 1

            # if sum is greater than zero than
            # decrement in right side
            else:
                r -= 1

    if (found == False):
        print(" No Triplet Found")


def find_unique_triplet(arr, sum):
    triplet_list = []
    arr_size=len(arr)
    # Fix the first element as A[i]
    for i in range(0, arr_size-2):
        # Fix the second element as A[j]
        for j in range(i+1, arr_size-1):
            # Now look for the third number
            for k in range(j+1, arr_size):
                if arr[i] + arr[j] + arr[k] == sum:
                    triplet = [arr[i], arr[j], arr[k]]
                    #print "Triplet is: {0}".format(triplet)
                    if not triplet in triplet_list:
                        triplet_list.append(triplet)

    return triplet_list


if __name__ == '__main__':
    a = [1, 2, -3, 5, 4, -9, 1, 2, -3]
    s = 0
    print find_unique_triplet(a, s) # [[1, 2, -3], [1, -3, 2], [2, -3, 1], [2, 1, -3], [-3, 1, 2], [5, 4, -9]]
    # without unique [[1, 2, -3], [1, 2, -3], [1, -3, 2], [1, 2, -3], [2, -3, 1], [2, 1, -3], [-3, 1, 2], [5, 4, -9], [1, 2, -3]]


    a = [1, 4, 45, 6, 10, 8]
    s = 22
    print find_triplet(a, s)
    """
    Triplet is: 4, 10, 8
    [(4, 10, 8)]
    """

    a = [1, 4, 45, 6, 10, 8]
    s = 15
    print find_triplet(a, s)

    """
    Triplet is: 1, 4, 10
    Triplet is: 1, 6, 8
    [(1, 4, 10), (1, 6, 8)]
    """



"""
another method:
https://www.geeksforgeeks.org/find-a-triplet-that-sum-to-a-given-value/
Time complexity of the method 1 is O(n^3). The complexity can be reduced to O(n^2) by
 sorting the array first, and then using method 1 of this post in a loop.
1) Sort the input array.
2) and then

# Python3 program to find a triplet
 
# returns true if there is triplet
# with sum equal to sum present
# in A[]. Also, prints the triplet
def find3Numbers(A, arr_size, sum):
 
    # Sort the elements 
    A.sort()
 
    # Now fix the first element 
    # one by one and find the
    # other two elements 
    for i in range(0, arr_size-2):
     
 
        # To find the other two elements,
        # start two index variables from
        # two corners of the array and
        # move them toward each other
         
        # index of the first element
        # in the remaining elements
        l = i + 1
         
        # index of the last element
        r = arr_size-1
        while (l < r):
         
            if( A[i] + A[l] + A[r] == sum):
                return True
             
            elif (A[i] + A[l] + A[r] < sum):
                l += 1
            else: # A[i] + A[l] + A[r] > sum
                r -= 1
 
    # If we reach here, then
    # no triplet was found
    return False

"""