import math
import os

file_name = 'blockinfo'
bitmap_file = 'bitmap2.bin'
volume_length = 42949672960  # Bytes  (40 GB)  # till here everything working
volume_length = 429496729600  # Bytes  (400(GB)  # working
volume_length = 1099511627776  # Bytes  (1 TB)    # Creates 16 MB bitmap file
#volume_length = 1125899906842624  # Bytes  (1 PB) # Taking very long time
block_size = 65536  # Bytes  (64 KB)


def write_chunk_of_zeros(file_path, chunk_size):
    chunk = (0 for i in range(chunk_size))
    with open(file_path, 'ab') as fp:
        fp.write(bytearray(chunk))


def create_bitmap_file(file_path, bitmap_size, chunk_size=1024*1024):
    print(f'bitmap_size: {bitmap_size}')

    if bitmap_size < chunk_size:
        write_chunk_of_zeros(file_path, bitmap_size)
    else:
        chunk_reminder = bitmap_size % chunk_size
        total_chunks = int(bitmap_size/chunk_size)
        print(f'total_chunks: {total_chunks}')

        for i in range(total_chunks):
            print(f'total chunks:{total_chunks}, chunk_size: {chunk_size}, Writing chunk no# {i}')
            write_chunk_of_zeros(file_path, chunk_size)

        print(f'Chunk reminder: {chunk_reminder}')
        if chunk_reminder != 0:
            write_chunk_of_zeros(file_path, chunk_reminder)

    print(f'Bit map File: {file_path} created successfully')


def read_in_chunks(file_object, chunk_size=1024*1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M."""
    while True:
        data = file_object.read(chunk_size)
        # print(f'Data len: {len(data)}')
        if not data:
            break
        yield data


def read_bitmap(file_path):
    bitmap_length = 0
    with open(file_path) as f:
        for data in read_in_chunks(f):
            bitmap_length += len(data)
    print(f'Bitmap length: {bitmap_length}')


def query_bitmap(file_path, offset, length):
    start = int(offset/block_size)
    count = int(length/block_size)
    with open(file_path, 'rb') as bitmap_fp:
        bitmap_fp.seek(start)
        data = bitmap_fp.read(count)
        print(f'Queried bitmap result: {data}')
        # print(data)


def update_bitmap(file_path, pos, bytes_array):
    with open(file_path, "r+b") as fp:
        fp.seek(pos)
        fp.write(bytes_array)
        print(f'Bitmap updated successfully')


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'File: {file_path} deleted successfully')


def convert_map():
    total_blocks = volume_length // block_size
    print(f'total_blocks: {total_blocks}')
    delete_file(bitmap_file)
    create_bitmap_file(bitmap_file, total_blocks)
    read_bitmap(bitmap_file)
    #return

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
    #convert_map()
    read_bitmap(bitmap_file)
    query_bitmap(bitmap_file, 1602289664, 131072)  # b'\x01\x01'
    query_bitmap(bitmap_file, 1108869120, 65536)  # b'\x01'
    query_bitmap(bitmap_file, 1602289664 - 65536, 65536 * 5)  # b'\x00\x01\x01\x00\x00'
    query_bitmap(bitmap_file, 16777216 - 65536, 65536)  # b'\x00\x01\x01\x00\x00'

    # with open(bitmap_file, 'rb') as fp:
    #     # total_blocks: 16777216
    #     fp.seek(16777215)
    #     print(fp.read(3))





