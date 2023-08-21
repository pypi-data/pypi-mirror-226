import numpy as np

FILE_NAME = 'savezCompressFile.npz'


def save_arrays(arr=10, size=10):
    with open(FILE_NAME, 'wb') as f:
        for i in range(arr):
            #nums = np.zeros(size, dtype=np.uint8)
            nums = [i for n in range(size)]
            np.savez_compressed(f, nums)  # but keep overwriting


def read_arrays(arr=10, size=10):
    with open(FILE_NAME, 'rb') as f:
        num = np.load(f)["arr_0"]
        print(num)  # [9 9 9 9 9 9 9 9 9 9]


if __name__ == '__main__':
    save_arrays()
    read_arrays()
    # num = np.load(FILE_NAME)['arr_0']
    # npzfile = np.load(FILE_NAME)
    # print(npzfile.files)  # ['arr_0']
    # print(npzfile.files[0]) # arr_0
    # print(npzfile['arr_0']) # [0 0 0 0 0 0 0 0 0 0]



