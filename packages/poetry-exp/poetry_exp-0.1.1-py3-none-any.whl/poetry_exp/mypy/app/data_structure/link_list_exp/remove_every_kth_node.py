"""
Remove every k-th node of the linked list
Given a singly linked list, Your task is to remove every K-th node of the linked list. Assume that K is always less than or equal to length of Linked List.

Examples :

Input : 1->2->3->4->5->6->7->8
        k = 3
Output : 1->2->4->5->7->8
As 3 is the k-th node after its deletion list
would be 1->2->4->5->6->7->8
And now 4 is the starting node then from it, 6
would be the k-th node. So no other kth node
could be there.So, final list is:
1->2->4->5->7->8.

Input: 1->2->3->4->5->6
       k = 1
Output: Empty list
All nodes need to be deleted

The idea is traverse the list from beginning and keep track of nodes visited after last deletion.
 Whenever count becomes k, delete current node and reset count as 0.

(1) Traverse list and do following
   (a) Count node before deletion.
   (b) If (count == k) that means current
        node is to be deleted.
      (i)  Delete current node i.e. do

          //  assign address of next node of
          // current node to the previous node
          // of the current node.
          prev->next = ptr->next i.e.

       (ii) Reset count as 0, i.e., do count = 0.
   (c) Update prev node if count != 0 and if
       count is 0 that means that node is a
       starting point.
   (d) Update ptr and continue until all
       k-th node gets deleted.

Node *deleteKthNode(struct Node *head, int k)
{
    // If linked list is empty
    if (head == NULL)
        return NULL;

    if (k == 1)
    {
       freeList(head);
       return NULL;
    }

    // Initialize ptr and prev before starting
    // traversal.
    struct Node *ptr = head, *prev = NULL;

    // Traverse list and delete every k-th node
    int count = 0;
    while (ptr != NULL)
    {
        // increment Node count
        count++;

        // check if count is equal to k
        // if yes, then delete current Node
        if (k == count)
        {
            // put the next of current Node in
            // the next of previous Node
            delete(prev->next);
            prev->next = ptr->next;

            // set count = 0 to reach further
            // k-th Node
            count = 0;
        }

        // update prev if count is not 0
        if (count != 0)
            prev = ptr;

        ptr = prev->next;
    }

    return head;
}

"""