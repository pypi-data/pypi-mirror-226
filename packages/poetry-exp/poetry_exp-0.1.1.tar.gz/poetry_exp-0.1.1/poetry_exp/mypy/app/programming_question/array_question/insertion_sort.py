"""
Algorithm	     Time Complexity
                 Best	      Worst
Heapsort	     o(nlog(n))	  O(nlog(n))
Bubble Sort	     o(n)         o(n^2)
Insertion sort   o(n)         o(n^2)


Insertion is faster than Bubble because of what occurs in each pass:
Bubble Sort swaps through all remaining unsorted values, moving one to the bottom.
"""

# Handles the duplicate as well
def insertion_sort(arr):
   for index in range(1,len(arr)):

     currentvalue = alist[index]
     position = index

     while position > 0 and arr[position-1] > currentvalue:
         arr[position] = arr[position-1]
         position = position-1

         arr[position] = currentvalue

     print 'i: ', index, 'List: ', arr


alist = [54, 26, 93, 17, 77, 31, 44, 55, 20, 17]
print alist
insertion_sort(alist)
print(alist)


"""
[54, 26, 93, 17, 77, 31, 44, 55, 20]
i:  1 List:  [26, 54, 93, 17, 77, 31, 44, 55, 20]
i:  2 List:  [26, 54, 93, 17, 77, 31, 44, 55, 20]
i:  3 List:  [17, 26, 54, 93, 77, 31, 44, 55, 20]
i:  4 List:  [17, 26, 54, 77, 93, 31, 44, 55, 20]
i:  5 List:  [17, 26, 31, 54, 77, 93, 44, 55, 20]
i:  6 List:  [17, 26, 31, 44, 54, 77, 93, 55, 20]
i:  7 List:  [17, 26, 31, 44, 54, 55, 77, 93, 20]
i:  8 List:  [17, 20, 26, 31, 44, 54, 55, 77, 93]
[17, 20, 26, 31, 44, 54, 55, 77, 93]
"""