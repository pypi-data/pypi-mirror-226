
def update_file(file_path, pos, bytes_array):
    with open(file_path, "r+b") as fp:
        fp.seek(pos)
        fp.write(bytes_array)
        print(f'File updated successfully')


def create_binary_file(file_path, file_size=2048, chunk_size=1024):
    chunk_counts = int(file_size/chunk_size)
    for i in range(int(chunk_counts)):
        chunk = (0 for i in range(chunk_size))
        with open(file_path, 'ab+') as fp:
            fp.write(bytearray(chunk))
            print(f'Writing chunk: {chunk}')
    print(f'File created successfully')


def read_file(file_path, bytes_count=10):
    with open(file_path, 'rb') as fp:
        data = fp.read()
        print(f'Data size: {len(data)} bytes')
        #print(f'Data: {data}')


if __name__ == '__main__':
    FILE_NAME = 'edit_big_binary_exp.bin'
    disk_size = 42949672960  # 40 GB
    # disk_size = 429496729600  # 400 GB
    # disk_size = 429496729600  # 400 GB
    disk_size = 1099511627776  # 1 TB

    block_size = 65536  # Bytes  (64(KB)
    bit_map_size = disk_size / block_size

    #create_binary_file(FILE_NAME, file_size=bit_map_size)
    read_file(FILE_NAME)

    update_file(FILE_NAME, 0, bytearray([1, 1]))
    read_file(FILE_NAME)
