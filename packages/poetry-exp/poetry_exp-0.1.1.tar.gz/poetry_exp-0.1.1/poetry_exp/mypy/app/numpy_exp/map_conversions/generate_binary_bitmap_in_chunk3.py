import math
file_name = 'blockinfo2'
bitmap_file = 'bitmap.bin'
volume_length = 48  # Bytes  (64(KB)
block_size = 2  # Bytes  (40 GB)


def create_bitmap_file(file_path, bitmap_size, chunk_size=2):
    if bitmap_size < chunk_size:
        chunk = (0 for i in range(bitmap_size))
        with open(file_path, 'ab+') as fp:
            fp.write(bytearray(chunk))
            print(f'Writing chunk: {chunk}')
    else:
        chunk_counts = bitmap_size/chunk_size
        for i in range(int(chunk_counts)):
            chunk = (0 for i in range(chunk_size))
            with open(file_path, 'ab+') as fp:
                fp.write(bytearray(chunk))
                print(f'total chunk:{chunk_counts}, chunk_size: {chunk_size}, Writing chunk# {i}: {chunk}')
    print(f'Bit map File: {file_path} created successfully')


def read_bitmap(file_path):
    with open(file_path, 'rb') as bitmap_fp:
        print('Bitmap:')
        data = bitmap_fp.read()
        print(f'Bitmap length: {len(data)}')
        print(data)


def update_bitmap(file_path, pos, bytes_array):
    with open(file_path, "r+b") as fp:
        fp.seek(pos)
        fp.write(bytes_array)
        print(f'Bitmap updated successfully')


def convert_map():
    total_blocks = volume_length // block_size
    print(f'total_blocks: {total_blocks}')
    create_bitmap_file(bitmap_file, total_blocks)
    read_bitmap(bitmap_file)

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

                print(f'block_counts: {block_counts}, start from : {start}')
                update_map = (1 for i in range(block_counts))
                print(f'Update bitmap, start: {start}, update_map length: {block_counts}')
                update_bitmap(bitmap_file, start, bytearray(update_map))




if __name__ == '__main__':
    convert_map()
    read_bitmap(bitmap_file)






