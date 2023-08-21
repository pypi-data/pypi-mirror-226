"""
Detect loop in a linked list
Given a linked list, check if the the linked list has loop or not. Below diagram shows a linked list with a loop.

1->2->3->4->5->2, 5 is not pointing to null, it is again pointing to one of the previous node

Approach1:
Use Hashing:
 - Traverse the list one by one and keep putting the node addresses in a Set.
 - At any point, if NULL is reached then return false and if next of current node points to
   any of the previously stored nodes in set then return true.
"""


# Python program to detect loop
# in the linked list

# Node class
class Node:
    # Constructor to initialize
    # the node object
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    # Function to initialize head
    def __init__(self):
        self.head = None

    # Function to insert a new
    # node at the beginning
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    # Utility function to prit
    # the linked LinkedList
    def printList(self):
        temp = self.head
        while (temp):
            print temp.data
            temp = temp.next

    def detectLoop(self):
        s = set()
        curr = self.head
        while (curr):

            # If we have already has
            # this node in hashmap it
            # means their is a cycle
            # (Because you we encountering
            # the node second time).
            if (curr in s):
                return True

            # If we are seeing the node for
            # the first time, insert it in hash
            s.add(curr)

            curr = curr.next

        return False


# Driver program for testing
llist = LinkedList()
llist.push(20)
llist.push(4)
llist.push(15)
llist.push(10)

# Create a loop for testing
llist.head.next.next.next.next = llist.head;

if (llist.detectLoop()):
    print ("Loop found")
else:
    print ("No Loop ")


"""
This is the fastest method. Traverse linked list using two pointers.
Move one pointer by one and other pointer by two.  
If these pointers meet at same node then there is a loop.
If pointers do not meet then linked list doesnt have loop.
"""


# Python program to detect loop in the linked list

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

    # Utility function to prit the linked LinkedList
    def printList(self):
        temp = self.head
        while (temp):
            print temp.data,
            temp = temp.next

    def detectLoop(self):
        slow_p = self.head
        fast_p = self.head
        while (slow_p and fast_p and fast_p.next):
            slow_p = slow_p.next
            fast_p = fast_p.next.next
            if slow_p == fast_p:
                print "Found Loop"
                return


# Driver program for testing
llist = LinkedList()
llist.push(20)
llist.push(4)
llist.push(15)
llist.push(10)

# Create a loop for testing
llist.head.next.next.next.next = llist.head
llist.detectLoop()