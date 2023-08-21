import os


def write_chunk_of_zeros(file_path, chunk_size):
    chunk = (0 for i in range(chunk_size))
    with open(file_path, 'ab') as fp:   # w+b, will overwrite every time
        fp.write(bytearray(chunk))


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        print(f'Data len: {len(data)}')
        if not data:
            break
        yield data


def read_file(file_path):
    data_len = 0
    with open(file_path, 'rb') as f:
        for data in read_in_chunks(f):
            data_len += len(data)
            #print(f'data: {data}')

    print(f'data_len: {data_len}')


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'File: {file_path} deleted successfully')


def create_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as fp:
           print(f'File: {file_path} created successfully')

if __name__ == '__main__':
    FILE_NAME = 'binary_file_in_chunks.bin'
    delete_file(FILE_NAME)
    create_file(FILE_NAME)

    chunk_size = 10240
    total_chunks = 64
    for i in range(64):
        #print(f'total chunks:{total_chunks}, chunk_size: {chunk_size}, Writing chunk no# {i}')
        write_chunk_of_zeros(FILE_NAME, chunk_size)
        # with open(FILE_NAME, 'rb') as f:
        #     print(len(f.read()))
    # write_chunk_of_zeros(FILE_NAME, 2)
    # write_chunk_of_zeros(FILE_NAME, 2)
    # write_chunk_of_zeros(FILE_NAME, 2)
    # write_chunk_of_zeros(FILE_NAME, 2)
    read_file(FILE_NAME)
    #
    # with open(FILE_NAME, 'rb') as f:
    #     print(len(f.read()))
