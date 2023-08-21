"""
Program for nth node from the end of a Linked List
Given a Linked List and a number n, write a function that returns the value at the nth node from end of the Linked List.
A->B->C->D->Null, 3rd element from end is B

Approach1:
- Calculate the length of the link list, let length is l
- Print the (l-n+1)th node from the begining of the linked list


Approach2:
- Maintain two pointers ref_ptr, main_ptr, and initilize both by head
- Traverse the list to nth time from the begining with ref_ptr
- Traverse the list again from the begening with main_ptr and ref_ptr till the ref_ptr reach to end
- Return the main_ptr

e.g let there are 10 nodes, need to find 3rd from the end, means(8)
move ref_ptr to three times, pointing to 3
move main_ptr and ref_ptr till ref_ptr reaches to end
ref_ptr will reach to end in 7th iteration
and main_ptr reaches to the 7th node- which is required pointer
"""


# Node class
class Node:
    # Constructor to initialize the node object
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    # Function to initialize head
    def __init__(self):
        self.head = None

    # Function to insert a new node at the beginning
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    def printNthFromLast(self, n):
        main_ptr = self.head
        ref_ptr = self.head

        count = 0
        if (self.head is not None):
            while (count < n):
                if (ref_ptr is None):
                    print "%d is greater than the no. pf \
                            nodes in list" % (n)
                    return

                ref_ptr = ref_ptr.next
                count += 1

        while (ref_ptr is not None):
            main_ptr = main_ptr.next
            ref_ptr = ref_ptr.next

        print "Node no. %d from last is %d " % (n, main_ptr.data)


# Driver program to test above function
llist = LinkedList()
llist.push(20)
llist.push(4)
llist.push(15)
llist.push(35)
llist.push(36)
llist.push(37)
llist.push(38)
llist.push(39)
llist.push(40)


llist.printNthFromLast(4)
