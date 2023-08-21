import math
import numpy as np

MAP_FILE = 'smallblockinfo'
BIT_MAP_FILE = 'smallDummyTextBitmap'
#volume_block_size = 2  # Bytes
volume_length = 42949672960  # Bytes  # Memory error for this: 1073741824000, 107374182400


def convert_map():
    # block_size = volume_block_size
    # total_blocks = volume_length // block_size
    # print(f'total_blocks: {total_blocks}')
    map = np.zeros(volume_length, dtype=np.int8)
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
                block_counts = vmware_length # number of blocks to read
                start = vmware_offset  # round up to lower value

                print(f'block_counts: {block_counts}, start from : {start}')
                i = 0
                while block_counts > 0:
                    map[start + i] = 1
                    block_counts -= 1
                    i += 1

    np.savetxt(BIT_MAP_FILE, [map], fmt='%d')


if __name__ == '__main__':
    convert_map()
    bitmap = np.loadtxt(BIT_MAP_FILE, dtype=int)[1:5]
    print(bitmap) # [1 0 0 1]
    #print(''.join([str(i) for i in bitmap]))
