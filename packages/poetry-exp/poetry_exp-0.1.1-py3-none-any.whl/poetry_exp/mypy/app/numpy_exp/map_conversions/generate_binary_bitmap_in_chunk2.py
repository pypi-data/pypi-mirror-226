import math
file_name = 'blockinfo2'
bitmap_file = 'sample_bitmap2.bin'
volume_length = 48  # Bytes  (64(KB)
block_size = 2  # Bytes  (40 GB)


def convert_map():
    total_blocks = volume_length // block_size
    print(f'total_blocks: {total_blocks}')

    first_line = True
    previous_offset = None
    previous_length = None
    with open(file_name) as map_fp:
        cbt_map = map_fp.read()
        if cbt_map:
            cbt_map_blocks = cbt_map.split()
            with open(bitmap_file, 'wb+') as trans_map_fp:
                for change_block in cbt_map_blocks:
                    change_block_arr = change_block.split(',')
                    vmware_offset = int(int(change_block_arr[0])/block_size)  # In bytes
                    vmware_length = int(int(change_block_arr[1])/block_size)  # in Bytes
                    print(f'vmware_offset: {vmware_offset}, vmware_length: {vmware_length}')

                    if first_line:
                        if vmware_offset != 0:
                            total_blocks = vmware_offset - 1
                            map = [0 for i in range(total_blocks)]
                            print(f'First line writing: {map}')
                            trans_map_fp.write(bytearray(map))

                    if not first_line:
                        if previous_offset + previous_length != vmware_offset:
                            total_blocks = vmware_offset - (previous_offset + previous_length)
                            map = [0 for i in range(total_blocks-1)]
                            print(f'Previous line writing: {map}')

                            trans_map_fp.write(bytearray(map))
                    first_line = False

                    map = [1 for i in range(vmware_length)]
                    print(f'Current line writing: {map}')

                    trans_map_fp.write(bytearray(map))
                    previous_offset = vmware_offset
                    previous_length = vmware_length

    # now look for remaining bytes


if __name__ == '__main__':
    convert_map()

    with open(bitmap_file, 'rb') as bitmap_fp:
        print('Reading file')
        print(bitmap_fp.read())




