import numpy as np
items = [1, 1, 0, 0, 1, 0, 0, 0, 1, 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

arr = np.array(items)
np.save('bitmap10', arr)

b = np.load('bitmap10.npy')[3:5]

print(b)