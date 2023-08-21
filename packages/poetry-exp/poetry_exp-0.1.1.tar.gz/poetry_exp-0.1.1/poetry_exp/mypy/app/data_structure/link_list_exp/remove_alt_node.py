"""
Delete alternate nodes of a Linked List
Given a Singly Linked List, starting from the second node delete all alternate nodes of it.
For example, if the given linked list is 1->2->3->4->5 then your function should convert it to 1->3->5,
 and if the given linked list is 1->2->3->4 then convert it to 1->3.

Method 1 (Iterative)
Keep track of previous of the node to be deleted. First change the next link of previous node
and then free the memory allocated for the node.

 void deleteAlt()
    {
       if (head == null)
          return;

       Node prev = head;
       Node curr = head.next;

       while (prev != null && curr != null)
       {
           /* Change next link of previus node */
           prev.next = curr.next;

           /* Free node */
           curr = null;

           /*Update prev and now */
           prev = prev.next;
           if (prev != null)
              curr = prev.next;
       }
    }

"""