class Node(object):

    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        return repr(self.data)


class DoublyLinkedList(object):

    def __init__(self):
        """ Create a new doubly linked list. Takes O(1) time. """
        self.head = None

    def prepend(self, data):
        """ Insert a new element at the beginning of the list. Takes O(1) time. """

        new_node = Node(data, next=self.head)
        if self.head:
            self.head.prev = new_node

        self.head = new_node

    def append(self, data):
        """ Insert a new element at the end of the list. Takes O(n) time. """

        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        curr = self.head
        while curr.next:
            curr = curr.next

        curr.next = new_node
        new_node.prev = curr

    def find(self, key):
        """ Search for the first element with `data` matching `key`.
         Return the element or `None` if not found. Takes O(n) time.
        """

        curr = self.head
        while curr and curr.data != key:
            curr = curr.next  # Will be None if not found

        return curr # # Will be None if not found

    def remove_elem(self, data_node):

        if data_node.prev:
            data_node.prev.next = data_node.next

        if data_node.next:
            data_node.next.prev = data_node.prev

        if data_node is self.head:
            self.head = data_node.next

        data_node.prev = None
        data_node.next =None

    def remove(self, key):
        """ Remove the first occurrence of `key` in the list. Takes O(n) time. """

        # curr = self.head
        # prev = None
        # while curr and curr.data != key:
        #     prev = curr
        #     curr = curr.next
        #
        # print curr
        # if prev is None:
        #     self.head = None
        # else:
        #     prev.next = curr.next
        # curr = None

        elem = self.find(key)
        if not elem:
            return
        self.remove_elem(elem)

    def reverse(self):
        """Reverse the list in-place. Takes O(n) time. """

        curr_node = self.head
        prev_node = None
        while curr_node:
            prev_node = curr_node.prev
            next_node = curr_node.next
            curr_node.prev = next_node
            curr_node.next = prev_node
            curr_node = next_node

        self.head = prev_node.prev

    def __repr__(self):
        curr = self.head
        l = []
        while curr:
            #print curr.data
            l.append(repr(curr))
            curr = curr.next
        return ", ".join(l)

if __name__ == '__main__':
    dl = DoublyLinkedList()
    dl.append(20)
    dl.append(30)
    dl.append(40)
    dl.prepend(10)
    print dl # 10, 20, 30, 40

    dl.remove(30)
    print dl # 10, 20, 40

    dl.reverse()
    print dl # 40, 20, 10
