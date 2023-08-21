import numpy as np

FILE_NAME = 'savezCompBigArrays.npz'


def save_arrays(total_arrays=10, size=10):
    arrays_items = {'arr_'+str(i): [] for i in range(total_arrays)}
    with open(FILE_NAME, 'wb') as f:
        for i in range(total_arrays):
            nums = np.zeros(size, dtype=np.uint8)
            #nums = [i for n in range(size)]
            arrays_items['arr_'+str(i)] = nums

        np.savez_compressed(f, **arrays_items)


def read_arrays(total_arrays=10, size=10):
    with open(FILE_NAME, 'rb') as f:
        for i in range(total_arrays):
            num = np.load(f)["arr_"+str(i)]
            print(num) # [9 9 9 9 9 9 9 9 9 9]



if __name__ == '__main__':
    # save_arrays()
    # read_arrays()
    vol_length = 42949672960 # 40 GB  Not working memory error
    vol_length = 1073741824  # 1 GB working, Created 1.1 GB file

    batch_size = 10000
    no_of_arrays = vol_length//batch_size
    save_arrays(total_arrays=no_of_arrays, size=batch_size) # memory Error
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

