"""
Delete middle of linked list
Given a singly linked list, delete middle of the linked list. For example, if given linked list is 1->2->3->4->5 then linked list should be modified to 1->2->4->5

If there are even nodes, then there would be two middle nodes, we need to delete the second middle element. For example, if given linked list is 1->2->3->4->5->6 then it should be modified to 1->2->3->5->6.

If the input linked list is NULL, then it should remain NULL.

If the input linked list has 1 node, then this node should be deleted and new head should be returned.

Approach:
The idea is to use two pointers, slow_ptr and fast_ptr.
Both pointers start from head of list.
When fast_ptr reaches end, slow_ptr reaches middle.
keep track of previous of middle so that we can delete middle.


struct Node* deleteMid(struct Node *head)
{
    // Base cases
    if (head == NULL)
        return NULL;
    if (head->next == NULL)
    {
        delete head;
        return NULL;
    }

    // Initialize slow and fast pointers to reach
    // middle of linked list
    struct Node *slow_ptr = head;
    struct Node *fast_ptr = head;

    // Find the middle and previous of middle.
    struct Node *prev; // To store previous of slow_ptr
    while (fast_ptr != NULL && fast_ptr->next != NULL)
    {
        fast_ptr = fast_ptr->next->next;
        prev = slow_ptr;
        slow_ptr = slow_ptr->next;
    }

    //Delete the middle node
    prev->next = slow_ptr->next;
    delete slow_ptr;

    return head;
}
"""