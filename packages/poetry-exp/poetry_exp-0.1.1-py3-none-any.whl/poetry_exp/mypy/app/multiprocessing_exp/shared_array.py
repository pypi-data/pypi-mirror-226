# https://www.geeksforgeeks.org/multiprocessing-python-set-2/
import multiprocessing


def square_array(shared_array):
    for i in range(len(shared_array)):
        shared_array[i] = shared_array[i] * shared_array[i]


if __name__ =='__main__':
    sa = multiprocessing.Array('i', 4)  # Array of int
    for i in range(len(sa)):
        sa[i] = i
    p1 = multiprocessing.Process(target=square_array, args=(sa,))
    p1.start()
    p1.join()
    print(sa)  # <SynchronizedArray wrapper for <multiprocessing.sharedctypes.c_long_Array_4 object at 0x05CC47B0>>


    for i in sa:
        print(i)