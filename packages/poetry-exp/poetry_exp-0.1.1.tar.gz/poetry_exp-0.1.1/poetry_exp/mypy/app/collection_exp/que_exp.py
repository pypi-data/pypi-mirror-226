class Queue(object):

    def __init__(self, q=None):
        self.q = q
        if self.q is None:
            self.q = []

    def append(self, element):
        self.q.append(element)

    def pop(self):
        return self.q.pop(0)

    def __len__(self):
        return len(self.q)

    def __str__(self):
        return "<type Queue> {0}".format(self.q)


q = Queue()
q.append(10)
q.append(20)
q.append(30)
q.append(40)
q.append(50)
print q  # <type Queue> [10, 20, 30, 40, 50]
print len(q) # 5


print q.pop() # 10
print q  # <type Queue> [20, 30, 40, 50]
print len(q) # 4
