"""

Check whether the length of given linked list is Even or Odd

Given a linklist, task is to make a function which check whether the length of linklist is even or odd.
Examples:

Input : 1->2->3->4->NULL
Output : Even

Input : 1->2->3->4->5->NULL
Output : Odd

Approach1: Traverse all the node and find the length and then calculate even or odd

Approach2:
Stepping 2 nodes at a time
1. Take a pointer and move that pointer two nodes at a time
2. At the end, if the pointer is NULL then length is Even, else Odd.

// Function to check the length of linklist
int LinkedListLength(struct Node* head)
{
    while (head && head->next)
    {
        head = head->next->next;
    }
    if (!head)
        return 0; #evene
    return 1;   # odd
}
"""