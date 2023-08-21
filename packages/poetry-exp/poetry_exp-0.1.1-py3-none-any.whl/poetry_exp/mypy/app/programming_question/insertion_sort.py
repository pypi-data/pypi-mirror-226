"""
Insertion sort is similar to arranging the documents of a bunch of students in order of their ascending roll number. Starting from the second element, we compare it with the first element and swap it if it is not in order. Similarly, we take the third element in the next iteration and place it at the right place in the sublist of the first and second elements (as the sublist containing the first and second elements is already sorted). We repeat this step with the fourth element of the list in the next iteration and place it at the right position in the sublist containing the first, second and the third elements. We repeat this process until our list gets sorted. So, the steps to be followed are:

Compare the current element in the iteration (say A) with the previous adjacent element to it. If it is in order then continue the iteration else, go to step 2.
Swap the two elements (the current element in the iteration (A) and the previous adjacent element to it).
Compare A with its new previous adjacent element. If they are not in order then proceed to step 4.
Swap if they are not in order and repeat steps 3 and 4.
Continue the iteration.
"""


a = [8, 16, 19, 11, 15, 10, 12, 14]

#iterating over a
for item in a:
    position = a.index(item)
    #position is not the first element
    while position>0:
        #not in order
        if a[position-1] > a[position]:
            #swap
            a[position-1],a[position] = a[position],a[position-1]
        else:
            #in order
            break
        position = position-1
print (a)


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