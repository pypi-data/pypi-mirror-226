import math
import os


def write_bits(bits_str, file_obj):
    print(f'Size of bits: {len(bits_str)}')
    i = 0
    buffer = bytearray()
    while i < len(bits_str):
        buffer.append(int(bits_str[i:i + 8], 2))
        i += 8

    # now write your buffer to a file
    file_obj.write(buffer)


def create_binary_bitmap(text_bitmap_file, bin_bitmap_file):
    bitmap_length = 0
    with open(text_bitmap_file) as tfp:
        with open(bin_bitmap_file, 'ab') as bfp:
            for bits_str in read_in_chunks(tfp):
                bitmap_length += len(bits_str)
                if bits_str:
                    write_bits(bits_str, bfp)
                else:
                    print('No bits found to write')

    print(f'Bitmap length: {bitmap_length}')


def write_chunk_of_zeros(file_path, chunk_size):
    chunk = (str(0) for i in range(chunk_size))
    with open(file_path, 'a') as fp:
        fp.write("".join(chunk))


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
    start = int(offset / BLOCK_SIZE)
    count = int(length / BLOCK_SIZE)
    with open(file_path, 'r') as bitmap_fp:
        bitmap_fp.seek(start)
        data = bitmap_fp.read(count)
        print(f'Queried bitmap result: {data}')
        # print(data)


def update_bitmap(file_path, pos, bits_str):
    with open(file_path, "r+") as fp:
        fp.seek(pos)
        fp.write(bits_str)
        print(f'Bitmap updated successfully')


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'File: {file_path} deleted successfully')


def convert_map():
    total_blocks = VOLUME_LENGTH // BLOCK_SIZE
    print(f'total_blocks: {total_blocks}')
    delete_file(BITMAP_TEXT_FILE_NAME)
    delete_file(BITMAP_BIN_FILE_NAME)

    create_bitmap_file(BITMAP_TEXT_FILE_NAME, total_blocks)
    read_bitmap(BITMAP_TEXT_FILE_NAME)

    with open(FILE_NAME) as map_fp:
        cbt_map = map_fp.read()
        if cbt_map:
            cbt_map_blocks = cbt_map.split()
            for change_block in cbt_map_blocks:
                change_block_arr = change_block.split(',')
                vmware_offset = int(change_block_arr[0])  # In bytes
                vmware_length = int(change_block_arr[1])  # in Bytes
                print(f'vmware_offset: {vmware_offset}, vmware_length: {vmware_length}')

                block_counts = math.ceil(vmware_length / BLOCK_SIZE)  # number of blocks to read
                start = math.ceil(vmware_offset / BLOCK_SIZE)

                print(f'block_counts: {block_counts}, start from : {start}')
                update_map = (str(1) for i in range(block_counts))
                print(f'Update bitmap, start: {start}, update_map length: {block_counts}')
                update_bitmap(BITMAP_TEXT_FILE_NAME, start, "".join(update_map))


if __name__ == '__main__':
    BITMAP_TEXT_FILE_NAME = 'bitmap3.txt'
    BITMAP_BIN_FILE_NAME = 'bitmap3.bin'

    # # Run small sample
    # FILE_NAME = 'blockinfo2'
    # VOLUME_LENGTH = 48  # Bytes
    # BLOCK_SIZE = 2  # Bytes  (64 KB)
    # convert_map()
    # read_bitmap(BITMAP_TEXT_FILE_NAME)
    # query_bitmap(BITMAP_TEXT_FILE_NAME, 0, 12)  # 110010
    # query_bitmap(BITMAP_TEXT_FILE_NAME, 2, 10)  # 10010
    # query_bitmap(BITMAP_TEXT_FILE_NAME, 6, 4)  # 01
    # query_bitmap(BITMAP_TEXT_FILE_NAME, 32, 12)  # 111100
    # query_bitmap(BITMAP_TEXT_FILE_NAME, 40, 8)  # 0000
    # create_binary_bitmap(BITMAP_TEXT_FILE_NAME, BITMAP_BIN_FILE_NAME)
    # with open(BITMAP_TEXT_FILE_NAME, 'r') as fp:
    #     print(fp.read())



    #
    # # Run Big sample
    FILE_NAME = 'blockinfo'
    VOLUME_LENGTH = 42949672960  # Bytes  (40 GB)
    # VOLUME_LENGTH = 429496729600  # Bytes  (400(GB)  # working
    VOLUME_LENGTH = 1099511627776  # Bytes  (1 TB)    # Creates 2 MB binary bitmap file
    # volume_length = 1125899906842624  # Bytes  (1 PB) # Taking very long time
    BLOCK_SIZE = 65536  # Bytes  (64 KB)
    convert_map()
    read_bitmap(BITMAP_TEXT_FILE_NAME)
    query_bitmap(BITMAP_TEXT_FILE_NAME, 0, 131072)  # 10
    query_bitmap(BITMAP_TEXT_FILE_NAME, 1602289664, 131072)  # 11
    query_bitmap(BITMAP_TEXT_FILE_NAME, 1108869120, 65536)  # 1
    query_bitmap(BITMAP_TEXT_FILE_NAME, 1602289664 - 65536, 65536 * 5)  # 01100
    query_bitmap(BITMAP_TEXT_FILE_NAME, 1099511627776 - 65536, 65536)  # 0
    create_binary_bitmap(BITMAP_TEXT_FILE_NAME, BITMAP_BIN_FILE_NAME)

    with open(BITMAP_TEXT_FILE_NAME, 'r') as fp:
        # total_blocks: 16777216
        fp.seek(16777215)
        print(fp.read(1))





