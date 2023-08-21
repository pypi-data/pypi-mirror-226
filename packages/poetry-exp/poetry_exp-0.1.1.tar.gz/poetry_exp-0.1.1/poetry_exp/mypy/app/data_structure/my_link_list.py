
class Node(object):
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return repr(self.data)


class SinglyLinkedList(object):

    def __init__(self):
        self.head = None

    def prepend(self, data):
        """Insert a new element at the beginning of the list. Takes O(1) time."""
        self.head = Node(data, next=self.head)

    def append(self, data):
        """Insert a new element at the end of the list. Takes O(n) time"""
        if not self.head:
            self.head = Node(data, next=None)
            return

        curr = self.head
        while curr.next:
            curr = curr.next

        curr.next = Node(data)

    def find(self, key):
        """ Search for the first element with `data` matching
        `key`. Return the element or `None` if not found. Takes O(n) time. """

        curr = self.head
        while curr and curr.data != key:
            curr = curr.next

        return curr

    def remove(self, key):
        """ Remove the first occurrence of `key` in the list. Takes O(n) time.
        Find the element and keep a # reference to the element preceding it

        """

        curr = self.head
        previous = None
        while curr and curr.data != key: # as the key matches, it stops the loops, will take the last loop values
            previous = curr
            curr = curr.next

        # unlink the element
        if previous is None: # means only one element
            self.head = curr.next
        else:
            previous.next = curr.next
            curr.next = None

    def revers(self):
        """ Reverse the list in-place. Takes O(n) time. """

        curr_node = self.head
        prev_node = None
        while curr_node:
            next_node = curr_node.next
            curr_node.next = prev_node
            prev_node = curr_node
            curr_node = next_node

        self.head = prev_node

    def __repr__(self):
        curr = self.head
        lst = []
        while curr:
            lst.append(repr(curr.data))
            curr = curr.next

        return ", ".join(lst)


if __name__ == '__main__':
    sl = SinglyLinkedList()
    sl.append(20)
    sl.append(30)
    sl.prepend(10)
    sl.append(40)
    sl.append(50)

    print sl # 10, 20, 30, 40, 50

    print sl.find(30)  # 30

    print sl.remove(30)
    print sl # 10, 20, 40, 50
    sl.revers()
    print '......', sl
