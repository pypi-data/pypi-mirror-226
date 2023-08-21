
def update_file(file_path, pos, bytes_array):
    with open(file_path, "r+b") as fp:
        fp.seek(pos)
        fp.write(bytes_array)
        print(f'File updated successfully')


def create_binary_file(file_path):
    data = (0 for i in range(100))
    with open(file_path, 'wb') as fp:
        fp.write(bytearray(data))
        print(f'File: {file_path} created successfully')


def read_file(file_path):
    with open(file_path, 'rb') as fp:
        data = fp.read()
        print(f'Length: {len(data)}')
        print(data)


if __name__ == '__main__':
    FILE_NAME = 'edit_binary_exp.bin'
    create_binary_file(FILE_NAME)
    read_file(FILE_NAME)

    update_map = (1 for i in range(5))
    update_file(FILE_NAME, 5, bytearray(update_map))
    update_file(FILE_NAME, 15, bytearray(update_map))
    update_file(FILE_NAME, 20, bytearray(update_map))

    read_file(FILE_NAME)
