import math
file_name = 'blockinfo'
volume_block_size = 65536  # Bytes  (64(KB)
volume_length = 42949672960  # Bytes  (40 GB)


def convert_map():
    block_size = volume_block_size
    total_blocks = volume_length // block_size
    print(f'total_blocks: {total_blocks}')
    map = [str(0) for i in range(total_blocks+1)]
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
                    map[start + i] = str(1)
                    block_counts -= 1
                    i += 1

    with open('transformed_map', 'w') as trans_map_fp:
        trans_map_fp.write(''.join(map))


if __name__ == '__main__':
    convert_map()