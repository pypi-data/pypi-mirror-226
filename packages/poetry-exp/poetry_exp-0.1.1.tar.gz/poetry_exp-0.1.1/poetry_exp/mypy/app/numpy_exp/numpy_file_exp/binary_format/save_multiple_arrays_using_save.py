import numpy as np

FILE_NAME = 'saveFile.npy'


def save_arrays(arr=10, size=10):
    with open(FILE_NAME, 'wb') as f:
        for i in range(arr):
            #nums = np.zeros(size, dtype=np.uint8)
            nums = [i for n in range(size)]
            np.save(f, nums)


def read_arrays(arr=10, size=10):
    with open(FILE_NAME, 'rb') as f:
        for i in range(arr):
            num = np.load(f)
            # If the file is a .npy file, then a single array is returned.
            print(num)


if __name__ == '__main__':
    #save_arrays()
    #read_arrays()

    npy_file = np.load(FILE_NAME)
    print(npy_file) # [0 0 0 0 0 0 0 0 0 0]

    npy_file = np.load(FILE_NAME)
    print(npy_file)  # [0 0 0 0 0 0 0 0 0 0]
    # print()
    # If the file is a .npy file, then a single array is returned.

    # npy_file = np.load(FILE_NAME, mmap_mode='r')
    # print(npy_file[1, :])


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