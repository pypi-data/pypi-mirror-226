"""
Count the number of possible triangles
Given an unsorted array of positive integers. Find the number of triangles that can be
formed with three different array elements as three sides of triangles.
For a triangle to be possible from 3 values, the sum of any two values (or sides)
must be greater than the third value (or third side).
For example, if the input array is {4, 6, 3, 7}, the output should be 3.
There are three triangles possible {3, 4, 6}, {4, 6, 7} and {3, 6, 7}. Note that {3, 4, 7}
 is not a possible triangle.
As another example, consider the array {10, 21, 22, 100, 101, 200, 300}.
There can be 6 possible triangles: {10, 21, 22}, {21, 100, 101},
 {22, 100, 101}, {10, 100, 101}, {100, 101, 200} and {101, 200, 300}


Apprach1: Find All Triplets and then check for sum of any two must be greater than the their value
Time Complexity: O(N^3) where N is the size of input array.


Approach2:
Method 2 (Tricky and Efficient)
Let a, b and c be three sides. The below condition must hold for a triangle
(Sum of two sides is greater than the third side)
i) a + b > c
ii) b + c > a
iii) a + c > b

Following are steps to count triangle.

Sort the array in non-decreasing order.

Initialize two pointers i and j to first and second elements respectively, and initialize count of triangles as 0.

Fix i and j and find the rightmost index k (or largest arr[k]) such that arr[i] + arr[j] > arr[k].
The number of triangles that can be formed with arr[i] and arr[j] as two sides is k-j. Add k-j to count of triangles

Let us consider arr[i] as a, arr[j] as b and all elements between arr[j+1] and arr[k] as c.
The above mentioned conditions (ii) and (iii) are satisfied because arr[i] < arr[j] < arr[k].
And we check for condition (i) when we pick k 4. Increment j to fix the second element again.

Note that in step 3, we can use the previous value of k. The reason is simple,
if we know that the value of arr[i] + arr[j-1] is greater than arr[k],
then we can say arr[i] + arr[j] will also be greater than arr[k], because the array is sorted in increasing order.

5. If j has reached end, then increment i. Initialize j as i + 1, k as i+2 and repeat the steps 3 and 4.

Following is implementation of the above approach.
Time Complexity: O(n^2). The time complexity looks more because of 3 nested loops.
If we take a closer look at the algorithm, we observe that k is initialized only once in the outermost loop.
The innermost loop executes at most O(n) time for every iteration of outer most loop, because k starts
from i+2 and goes upto n for all values of j. Therefore, the time complexity is O(n^2).
"""



def find_possible_triangles(arr):
    size = len(arr)
    count = 0
    for i in range(0, size-2):
        for j in range(i+1, size-1):
            for k in range(j+1, size):
                if arr[i] + arr[j] > arr[k]:
                    count += 1
                    print "Triangle: ", arr[i], arr[j], arr[k]
    print count


def findnumberofTriangles(arr):
    # Sort array and initialize count as 0
    n = len(arr)
    arr.sort()
    count = 0

    # Fix the first element.  We need to run till n-3 as
    # the other two elements are selected from arr[i+1...n-1]
    for i in range(0, n - 2):

        # Initialize index of the rightmost third element
        k = i + 2

        # Fix the second element
        for j in range(i + 1, n):

            # Find the rightmost element which is smaller
            # than the sum of two fixed elements
            # The important thing to note here is, we use
            # the previous value of k. If value of arr[i] +
            # arr[j-1] was greater than arr[k], then arr[i] +
            # arr[j] must be greater than k, because the array
            # is sorted.
            while (k < n and arr[i] + arr[j] > arr[k]):
                k += 1

                # Total number of possible triangles that can be
                # formed with the two fixed elements is k - j - 1.
                # The two fixed elements are arr[i] and arr[j]. All
                # elements between arr[j+1] to arr[k-1] can form a
                # triangle with arr[i] and arr[j]. One is subtracted
                # from k because k is incremented one extra in above
                # while loop. k will always be greater than j. If j
                # becomes equal to k, then above loop will increment k,
                #  because arr[k] + arr[i] is always greater than arr[k]
            count += k - j - 1

    return count


if __name__ == "__main__":
    l = [4, 6, 3, 7]
    find_possible_triangles(l)

"""
Triangle:  4 6 3
Triangle:  4 6 7
Triangle:  6 3 7
3
"""