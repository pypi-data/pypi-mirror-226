import numpy as np

FILE_NAME = 'savezCompress2File.npz'


def save_arrays(arr=10, size=10):
    arrays_items = {'arr_'+str(i): [] for i in range(10)}
    with open(FILE_NAME, 'wb') as f:
        for i in range(arr):
            #nums = np.zeros(size, dtype=np.uint8)
            nums = [i for n in range(size)]
            arrays_items['arr_'+str(i)] = nums

        np.savez_compressed(f, **arrays_items)


def read_arrays(arr=10, size=10):
    with open(FILE_NAME, 'rb') as f:
        for i in range(arr):
            num = np.load(f)["arr_"+str(i)]
            print(num) # [9 9 9 9 9 9 9 9 9 9]



if __name__ == '__main__':
    # save_arrays()
    read_arrays()

"""
[0 0 0 0 0 0 0 0 0 0]
[1 1 1 1 1 1 1 1 1 1]
[2 2 2 2 2 2 2 2 2 2]
[3 3 3 3 3 3 3 3 3 3]
[4 4 4 4 4 4 4 4 4 4]
[5 5 5 5 5 5 5 5 5 5]
[6 6 6 6 6 6 6 6 6 6]
[7 7 7 7 7 7 7 7 7 7]
[8 8 8 8 8 8 8 8 8 8]
[9 9 9 9 9 9 9 9 9 9]
"""

