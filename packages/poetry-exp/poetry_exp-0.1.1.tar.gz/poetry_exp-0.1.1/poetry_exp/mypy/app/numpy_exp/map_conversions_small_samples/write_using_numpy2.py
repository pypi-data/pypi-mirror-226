import numpy as np
items = [1, 1, 0, 0, 1, 0, 0, 0, 1, 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

arr = np.array(items)
#np.savetxt('bitmaptext.csv', [arr], fmt='%d')
np.save('array.csv', [arr])

# b = np.loadtxt('test1.txt', dtype=int)
# print(b)  # [1 1 0 0 1 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
#
# print(b[3:5])  #01
# print(b[1:6])  #[1 0 0 1 0]

#b = np.loadtxt('array.csv.npy', dtype=int)[3:5]
b = np.load('array.csv.npy')[0][3:5]


#b = np.fromfile('array.csv', dtype=int, count=2, offset=3)
print(b)