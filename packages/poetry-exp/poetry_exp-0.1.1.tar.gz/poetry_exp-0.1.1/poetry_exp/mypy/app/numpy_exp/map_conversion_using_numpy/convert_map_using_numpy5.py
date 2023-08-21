import math
import numpy as np
import time

MAP_FILE = 'blockinfo'
#BIT_MAP_FILE = '100GbTextBitmap'  # 3.12 MB to store 1638400 bits
BIT_MAP_FILE = '1000GbTextBitmap'  # 31.2 MB to store 16384000 bits

volume_block_size = 65536  # Bytes  (64 KB)
# volume_length = 42949672960  # Bytes  (40 GB)
#volume_length = 107374182400  # Bytes  (100 GB)
volume_length = 1073741824000  # Bytes  (1000 GB)


def convert_map():
    block_size = volume_block_size
    total_blocks = volume_length // block_size
    print(f'total_blocks: {total_blocks}')
    map = np.zeros(total_blocks, dtype=int)
    #print(f'map: {map}')
    with open(MAP_FILE) as map_fp:
        cbt_map = map_fp.read()
        if cbt_map:
            cbt_map_blocks = cbt_map.split()
            for change_block in cbt_map_blocks:
                change_block_arr = change_block.split(',')
                vmware_offset = int(change_block_arr[0])  # In bytes
                vmware_length = int(change_block_arr[1])  # in Bytes
                print(f'vmware_offset: {vmware_offset}, vmware_length: {vmware_length}')

                # round up to upper value
                block_counts = math.ceil(vmware_length / block_size)  # number of blocks to read
                start = vmware_offset // block_size  # round up to lower value

                print(f'block_counts: {block_counts}, start from : {start}')
                i = 0
                while block_counts > 0:
                    map[start + i] = 1
                    block_counts -= 1
                    i += 1

    np.savetxt(BIT_MAP_FILE, [map], fmt='%d')


if __name__ == '__main__':
    t1 = time.time()

    #convert_map()

    bitmap = np.loadtxt(BIT_MAP_FILE, dtype=int)[1:5]
    print(bitmap) # [1 0 0 1]
    t2 = time.time()
    print(f'Time taken: {t2-t1}')  # 40 sec for 1000 GB, 4 sec for 100 GB
    #print(''.join([str(i) for i in bitmap]))
