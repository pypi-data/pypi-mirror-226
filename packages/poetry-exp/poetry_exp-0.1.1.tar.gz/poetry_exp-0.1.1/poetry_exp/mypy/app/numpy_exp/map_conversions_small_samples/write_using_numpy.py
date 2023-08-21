import numpy as np
newFileBytes = [1, 1, 0, 0, 1, 0, 0, 0, 1, 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

# a = np.array(newFileBytes)
# # np.savetxt('test1.txt', a, fmt='%08d')  # will save 1 to 00000001
# np.savetxt('test1.txt', a, fmt='%d', delimiter='\t')

# b = np.loadtxt('test1.txt', dtype=int)
# print(b)  # [1 1 0 0 1 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
#
# print(b[3:5])  #01
# print(b[1:6])  #[1 0 0 1 0]


b = np.fromfile('test1.txt', dtype=int, count=2, offset=3)
print(b)