import math
file_name = 'blockinfo'
volume_block_size = 65536  # Bytes  (64(KB)
volume_length = 42949672960  # Bytes  (40 GB)


def convert_map():
    block_size = volume_block_size
    total_blocks = volume_length // block_size
    print(f'total_blocks: {total_blocks}')
    map = [0 for i in range(total_blocks+1)]
    #print(f'map: {map}')
    with open(file_name) as map_fp:
        cbt_map = map_fp.read()
        if cbt_map:
            cbt_map_blocks = cbt_map.split()
            for change_block in cbt_map_blocks:
                change_block_arr = change_block.split(',')
                vmware_offset = int(change_block_arr[0])  # In bytes
                vmware_length = int(change_block_arr[1])  # in Bytes
                print(f'vmware_offset: {vmware_offset}, vmware_length: {vmware_length}')

                block_counts = math.ceil(vmware_length / block_size)  # number of blocks to read
                start = math.ceil(vmware_offset / block_size)
                #
                # block_counts = vmware_length / block_size  # number of blocks to read
                # start = vmware_offset / block_size
                print(f'block_counts: {block_counts}, start from : {start}')
                i = 0
                while block_counts > 0:
                    map[start + i] = 1
                    block_counts -= 1
                    i += 1

    with open('sample_bitmap.bin', 'wb') as trans_map_fp:
        print(f'Writing the bit map of size: {len(map)}, type: {type(map)}')
        trans_map_fp.write(bytearray(map))


if __name__ == '__main__':
    convert_map()

    dummy_map = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    dummy_bitmap_file = 'dummy_binary_bitmap.bin'
    # with open(dummy_bitmap_file, 'wb') as trans_map_fp:
    #     trans_map_fp.write(bytearray(dummy_map))

    # with open(dummy_bitmap_file, 'wb') as trans_map_fp:
    #     for bit in dummy_map:
    #         trans_map_fp.write(bytearray([bit]))
    #     trans_map_fp.write(bytearray(dummy_map))
    #
    # with open('binary_bitmap.bin', 'rb') as bitmap_fp:
    #     print('Reading file')
    #     #print(bitmap_fp.read(1))  # b'\x01'
           # b'\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00'
        # with open('test', 'w') as tf:
        #     tf.write(str(bitmap_fp.read()))



