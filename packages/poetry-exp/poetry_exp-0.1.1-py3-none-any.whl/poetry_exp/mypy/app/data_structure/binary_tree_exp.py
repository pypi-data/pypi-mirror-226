"""
https://www.tutorialspoint.com/python/python_binary_tree.htm
- Tree is a special form of graph
  Linear means: where we have logical start and logical end points of Data structure

Unlike linked list, stack queues, Tree is non-linear data structure, it is  hierarchical data structures.
The topmost node is called root of the tree. The elements that are directly under an element are called its children.

- Used to store information that naturally forms a hierarchy. For example, the file system on a computer:
  Router algorithms, multi-stage decision-making, for compositing digital images for visual effects.

-  Trees (with some ordering e.g., BST) provide moderate access/search (quicker than Linked List and slower than arrays).
-  Trees provide moderate insertion/deletion (quicker than Arrays and slower than Unordered Linked Lists).
-  Like Linked Lists and unlike Arrays, Trees dont have an upper limit on number of nodes as nodes are linked using pointers.

Binary Tree:
  - A tree whose elements have at most 2 children is called a binary tree.
  - Since each element in a binary tree can have only 2 children, we typically name them the left and right child.
  - Binary trees are special cases of tree where every node has at most two children.

Types of binary tree:
 1. Full Binary Tree: Each node has 0 or two children
     No. of leaf nodes = No of internal node(which has some child) +1

 2. Complete Binary Tree: if all levels are completely filled except possibly the
   last level and the last level has all keys as left as possible

 3. Perfect Binary Tree: All internal nodes have two children and all leaves are at same level
    No of nodes = 2^h-1 , h is the height of the tree

 4. Balanced Binary tree: A binary tree is balanced if the height of the tree is O(Log n) , n is no of node
   -  Balanced Binary Search trees are performance wise good as they provide O(log n) time for search, insert and delete.

 5. A degenerate (or pathological) tree A Tree where every internal node has one child.
    Such trees are performance-wise same as linked list


Tree Traversal: unlike liked list, stack ques, Trees can be traversed in following order using Depth First Traversals
  or Breadth first Traversal

  1. Depth First traversal:
      a. Inorder: left, root, right
      b. Preorder: root, left, right
      c. Postorder: left, right, root
      Time complexity for all traversal is o(N) because you are hitting each node once,
      Since a Binary Tree is also a Graph, the same applies here.
      The complexity of each of these Depth-first traversals is O(n+m). m is no of edges
      in binary tree max no of edges = n-1, n is no of node


  2. Breadth first or level order traversal: Traverse level by level
      start from root then its left and right and then make root'sleft as root
"""


class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.right = right
        self.left = left


def traverse_inorder(root):
    if root:
        traverse_inorder(root.left)
        print root.data
        traverse_inorder(root.right)

    """
    Explanations: first check if root is not null and 
    """


def traverse_preorder(root):
    if root:
        print root.data
        traverse_preorder(root.left)
        traverse_preorder(root.right)
    """"
    Explanations: first check if root is not null, then print it and then move towards left
    and then again check it it is not null, print it and move towards its left
    and if its left is null, move to its right, and if its right is null, move back to its root
    """

def traverse_postorder(root):
    if root:
        traverse_postorder(root.left)
        traverse_postorder(root.right)
        print root.data


# If you want all the data
def traverse_inorder2(root, data = []):
    if root:
        traverse_inorder(root.left)
        data.append(root.data)
        traverse_inorder(root.right)
    return data


"""
A Binary Search Tree has a very specific property: for any node X, Xs data is larger than the data
 of any descendent of its left child, and smaller than the data of any descendant of its right child.
"""


class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(self.root, data)

    def _insert(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert(node.right,data)

    def print_tree(self):
        if self.root:
            self._print_tree(self.root)

    def _print_tree(self, node):
        if node:
            self._print_tree(node.left)
            print( node.data),
            self._print_tree(node.right)

    def find(self, data):
        if self.root is None:
            return "Not found"
        else:
            return self._find(self.root, data)

    def _find(self, node, data):
        if node:
            if data < node.data:
                if node.left is None:
                    return "Not found"
                else:
                    return self._find(node.left, data)
            elif data > node.data:
                if node.right is None:
                    return "Not found"
                else:
                    return self._find(node.right, data)
            else:
                return "Found"
        else:
            return "Not found"


class BinarySearchTreeV2(object):
    val = None
    left = None
    right = None

    def __init__(self, val):
        self.val = val

    def insert(self, val):
        if self.val is not None:
            if val < self.val:
                if self.left is not None:
                    self.left.insert(val)
                else:
                    self.left = BinarySearchTreeV2(val)
            elif val > self.val:
                if self.right is not None:
                    self.right.insert(val)
                else:
                    self.right = BinarySearchTreeV2(val)
            else:
                return
        else:
            self.val = val
            print("new node added")

    # Inorder
    def showTree(self):
        if self.left:
            self.left.showTree()
        print(self.val),
        if self.right:
            self.right.showTree()

def demo1():
    # e.g 1 Tree with five node
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    print '.........Inorder.........'
    traverse_inorder(root)  # 4 2 5 1 3
    print '.........Preorder.........'
    traverse_preorder(root)  # 1 2 4 5 3
    print '.........Postorder.........'
    traverse_postorder(root)  # 4 5 2 3 1

    # Same tree if traverse by Breadth first serch: then it is 1,2,3,4,5

    # e.g 1 Tree with six node
    root = Node('A')
    root.left = Node('B')
    root.right = Node('C')
    root.left.left = Node('D')
    root.left.right = Node('E')
    root.left.right.left = Node('F')
    print '.........Inorder.........'
    traverse_inorder(root)  # D B F E A C
    print '.........Preorder.........'
    traverse_preorder(root)  # A B D E F C
    print '.........Postorder.........'
    traverse_postorder(root)  # D F E B C A


if __name__ == '__main__':
    # demo1()

    #
    bt = BinarySearchTree()
    bt.insert(10)
    bt.insert(5)
    bt.insert(15)
    bt.insert(3)
    bt.insert(20)
    bt.print_tree()  # 3 5 10 15 20

    print bt.find(15)
    print bt.find(30)


    print '\nversion 2'
    bt = BinarySearchTreeV2(10)
    bt.insert(5)
    bt.insert(15)
    bt.insert(3)
    bt.insert(20)
    bt.showTree() # 3, 5, 10 15, 20
