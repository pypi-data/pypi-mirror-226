
file_name = 'blockinfo'
volume_block_size = 4096 # 4K
volume_length = 100 * 1024 * 1024 * 8  # 100M


def convert_map():
    block_size = volume_block_size * 8
    map_length = volume_length // block_size
    print(f'map_length: {map_length}')
    map = [str(0) for i in range(map_length+1)]
    print(f'map: {map}')
    with open(file_name) as map_fp:
        cbt_map = map_fp.read()
        if cbt_map:
            cbt_map_blocks = cbt_map.split()
            for change_block in cbt_map_blocks:
                change_block_arr = change_block.split(',')
                vmware_offset = int(change_block_arr[0])
                vmware_length = int(change_block_arr[1])
                print(f'vmware_offset: {vmware_offset}, vmware_length: {vmware_length}')

                start = vmware_offset // block_size
                print(f'.........start: {start}')
                print(f'.......vmware_offset + vmware_length: {vmware_offset + vmware_length}')
                end = (vmware_offset + vmware_length) // block_size
                print(f'start: {start}, end: {end}')
                for i in range(start, end):
                    map[i] = str(1)

    with open('transformed_map', 'w') as trans_map_fp:
        trans_map_fp.write(''.join(map))


if __name__ == '__main__':
    convert_map()