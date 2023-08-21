"""
Remove duplicates from an unsorted linked list
Write a removeDuplicates() function which takes a list and deletes any duplicate nodes from the list. The list is not sorted.

For example if the linked list is 12->11->12->21->41->43->21 then removeDuplicates() should convert the list to 12->11->21->41->43.

Approach1: Use Two Loops
 - Pick the first node and compare it with all all other nodes
 - Outer loop is used to pick the elements one by one and inner loop
    compares the picked element with rest of the elements.

Time Complexity: O(n^2)

Approach2:
 - Sort the Linked List(using merge sort)
 - Traverse the list
 - While Traversing , comapre the current node with the next node
 - If it matches, delete the next node
 - Before deleting, store the next pointer of the node
Time Complexity: O(nLogn)

Approach3: (Use Hashing)
 - We traverse the link list from head to end.
 - For every newly encountered element, we check whether it is in the hash table
    if yes, we remove it; otherwise we put it in the hash table.

  static void removeDuplicate(node head)
    {
        // Hash to store seen values
        HashSet<Integer> hs = new HashSet<>();

        /* Pick elements one by one */
        node current = head;
        node prev = null;
        while (current != null)
        {
            int curval = current.val;

             // If current value is seen before
            if (hs.contains(curval)) {
                prev.next = current.next;
            } else {
                hs.add(curval);
                prev = current;
            }
            current = current.next;
        }

    }
Time Complexity: O(n) on average (assuming that hash table access time is O(1) on average).


"""