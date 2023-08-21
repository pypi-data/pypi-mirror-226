# https://www.geeksforgeeks.org/multiprocessing-python-set-2/
import multiprocessing


def square_sum(l, square_sum):
    for idx, val in enumerate(l):
        l[idx] = val * val
    square_sum.value = sum(l)


if __name__ == '__main__':
    l = [1, 2, 3, 4]
    square_result = multiprocessing.Value('i')  # integer
    p1 = multiprocessing.Process(target=square_sum, args=(l, square_result))
    p1.start()
    p1.join()
    print(square_result)  # <Synchronized wrapper for c_long(30)>
    print(square_result.value)   # 30
