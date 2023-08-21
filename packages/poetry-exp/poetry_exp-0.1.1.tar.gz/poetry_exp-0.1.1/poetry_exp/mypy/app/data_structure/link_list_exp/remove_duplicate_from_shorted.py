"""
Remove duplicates from a sorted linked list
Write a removeDuplicates() function which takes a list sorted in non-decreasing order
and deletes any duplicate nodes from the list. The list should only be traversed once.

For example if the linked list is 11->11->11->21->43->43->60 then removeDuplicates() should convert the list to 11->21->43->60.

Approach1:
 - Traverse the list from the head (or start) node.
 - While traversing, compare current node with its next node.
 - If data of next node is same as current node then delete the next node.
 - Before we delete a node, we need to store next pointer of the node

  while (current->next != NULL)
    {
       /* Compare current node with next node */
       if (current->data == current->next->data)
       {
           /* The sequence of steps is important*/
           next_next = current->next->next;
           free(current->next);
           current->next = next_next;
       }
       else /* This is tricky: only advance if no deletion */
       {
          current = current->next;
       }
    }

Time Complexity: O(n) where n is number of nodes in the given linked list.
"""