
"""
Find a triplet from three linked lists with sum equal to a given number
Given three linked lists, say a, b and c, find one node from each list such that
the sum of the values of the nodes is equal to a given number.

For example, if the three linked lists are 12->6->29, 23->5->8 and 90->20->59,
and the given number is 101, the output should be tripel 6 5 90.

In the following solutions, size of all three linked lists is assumed same for simplicity of analysis.
 The following solutions work for linked lists of different sizes also.

A simple method to solve this problem is to run three nested loops.
The outermost loop picks an element from list a, the middle loop picks an element from b
and the innermost loop picks from c. The innermost loop also checks whether the sum of values
of current nodes of a, b and c is equal to given number.
The time complexity of this method will be O(n^3).

Sorting can be used to reduce the time complexity to O(n*n). Following are the detailed steps.
1) Sort list b in ascending order, and list c in descending order.
2) After the b and c are sorted, one by one pick an element from list a and
find the pair by traversing both b and c. See isSumSorted() in the following code.
The idea is similar to Quadratic algorithm of 3 sum problem.

Following code implements step 2 only. The solution can be easily modified for unsorted
 lists by adding the merge sort code discussed here


boolean isSumSorted(LinkedList la, LinkedList lb, LinkedList lc,
                       int givenNumber)
   {
      Node a = la.head;

      // Traverse all nodes of la
      while (a != null)
      {
          Node b = lb.head;
          Node c = lc.head;

          // for every node in la pick 2 nodes from lb and lc
          while (b != null && c!=null)
          {
              int sum = a.data + b.data + c.data;
              if (sum == givenNumber)
              {
                 System.out.println("Triplet found " + a.data +
                                     " " + b.data + " " + c.data);
                 return true;
              }

              // If sum is smaller then look for greater value of b
              else if (sum < givenNumber)
                b = b.next;

              else
                c = c.next;
          }
          a = a.next;
      }
      System.out.println("No Triplet found");
      return false;
   }
"""

