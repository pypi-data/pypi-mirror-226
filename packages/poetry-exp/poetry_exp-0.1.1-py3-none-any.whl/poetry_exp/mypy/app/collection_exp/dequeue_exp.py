"""
deque provides you with a double ended queue which means that you can append
and delete elements from either side of the queue.
"""

from collections import deque

dq = deque()
dq.append(10)
dq.append(20)
dq.append(30)

print len(dq) # 3

print dq[0] # 10
print dq[-1] # 30

# Pop values from both side
dq = deque(range(5))
print len(dq) # 5

print dq.popleft() # 0
print dq.pop() # 4

# limit the amount of items a deque can hold
dq = deque(maxlen=5)
dq.append(10)
dq.append(20)
dq.append(30)
dq.append(40)
dq.append(50)
dq.append(60) # will replace the fists one
dq.append(70) # will replace the second one
dq.append(80)
dq.append(90)

print dq # deque([50, 60, 70, 80, 90], maxlen=5)

"""
Now whenever you insert values after 30, the leftmost value will be popped from the
list. You can also expand the list in any direction with new values:

"""

d = deque([1,2,3,4,5])
d.extendleft([0])
d.extend([6,7,8])
print(d)

# Output: deque([0, 1, 2, 3, 4, 5, 6, 7, 8])