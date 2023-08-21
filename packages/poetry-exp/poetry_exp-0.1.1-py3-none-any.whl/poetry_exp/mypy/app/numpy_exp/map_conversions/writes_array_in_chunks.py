import math
FILE_NAME = 'chunked_map'


def writes_array_in_chunks(arr, chunk_size):
    if len(arr) < chunk_size:
        with open(FILE_NAME, 'wb') as fp:
            fp.write(bytearray(arr))
    else:
        total_chunk = math.ceil(len(arr)/chunk_size)
        print(f'Total chunk: {total_chunk}')
        start_index = 0
        with open(FILE_NAME, 'wb+') as fp:
            for i in range(total_chunk):
                chunk = arr[start_index: start_index+chunk_size]
                print(list(chunk))
                fp.write(bytearray(list(chunk)))
                start_index += chunk_size



def writes_array_in_chunks_text(arr, chunk_size):
    if len(arr)< chunk_size:
        with open(FILE_NAME, 'w') as fp:
            fp.write(" ".join(arr))
    else:
        total_chunk = math.ceil(len(arr)/chunk_size)
        print(f'Total chunk: {total_chunk}')
        start_index = 0
        with open(FILE_NAME, 'w') as fp:
            for i in range(total_chunk):
                chunk = arr[start_index: start_index+chunk_size]
                print(chunk)
                fp.write(" ".join(chunk))
                fp.write("\n")

                start_index += chunk_size


if __name__ == '__main__':
    nums = [0 for i in range(100)]
    writes_array_in_chunks(nums, 10)

    with open(FILE_NAME, 'rb') as fp:
        for line in fp.readlines():
            print(line)   # For binary files, will give all in one line

    # nums = [str(i) for i in range(100)]
    # writes_array_in_chunks_text(nums, 10)





