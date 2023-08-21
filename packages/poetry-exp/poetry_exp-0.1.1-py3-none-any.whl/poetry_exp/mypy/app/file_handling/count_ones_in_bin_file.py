import numpy as np

def count_ones(file_name):
    count = 0
    f = open(file_name, "rb")
    #nums = np.fromfile(f, dtype=np.uint32)
    nums  = np.load(f, allow_pickle=True)
    # for n in nums:
    #     print(n)
    print(len([1 for bit in nums if bit=='1']))

import struct
from array import array
from bitstring import ConstBitStream, BitArray

def count_ones_in_file(file_name):
    count = 0
    # read file
    b = ConstBitStream(filename=file_name)

    # read 5 bits
    output = b.read(102400)
    for s in str(output):
        print(s)
        if s == '1':
            count += 1
    print(count)
    #
    # # convert to unsigned int
    # integer_value = output.uint
    # print(integer_value)


def bits(f):
    bytes = (ord(b) for b in f.read())
    for b in bytes:
        for i in range(8):
            yield (b >> i) & 1


def count2(file_name):
    count = 0
    zero_count = 0
    for b in bits(open(file_name, 'r')):
        if b == 1:
            count += 1
        elif b==0:
            zero_count +=1
        else:
            raise Exception("Invalid char")
        #print (b)

    print(f'Ones: {count}')
    print(f'Zeros: {zero_count}')


def count3(file_name):
    b = BitArray(bytes=open(file_name, 'rb').read())
    #print(b.bin)
    zero_count = 0
    one_count = 1
    for bit in b.bin:
       if bit == '1':
           one_count += 1
       elif bit == '0':
           zero_count += 1
       else:
           raise Exception("Invalid char")

    print(f'Ones: {one_count}')
    print(f'Zeros: {zero_count}')

if __name__ == '__main__':
    #count_ones_in_file('f54720d1-2e45-47d4-91c1-3e7acaa296bf.bin')
    count2('f54720d1-2e45-47d4-91c1-3e7acaa296bf.bin')
    #count3('f54720d1-2e45-47d4-91c1-3e7acaa296bf.bin')
