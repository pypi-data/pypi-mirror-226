"""
Find the middle of a given linked list.
Given a singly linked list, find middle of the linked list.
For example, if given linked list is 1->2->3->4->5 then output should be 3.
If there are even nodes, then there would be two middle nodes, we need to print second middle element.
For example, if given linked list is 1->2->3->4->5->6 then output should be 4.

Approach1:
- Traverse the whole linked list and count the no. of nodes.
- Now traverse the list again till count/2 and return the node at count/2.

Approach2:
 - Traverse linked list using two pointers.
 - Move one pointer by one and other pointer by two.
 - When the fast pointer reaches end slow pointer will reach middle of the linked list
"""