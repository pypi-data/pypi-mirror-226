
def update_file(file_path, pos, new_str):
    with open(file_path, "r+") as fp:
        fp.seek(pos)
        fp.write(new_str)
        print(f'File updated successfully')


def read_from_pos(file_path, pos, bytes_counts):
    with open(file_path, "r") as fp:
        fp.seek(pos)
        data = fp.read(bytes_counts)
        print(f'Data: {data}')  # FA


if __name__ == '__main__':
    FILE_NAME = 'edit_file_exp.txt'
    #update_file(FILE_NAME, 2, 'F')
    read_from_pos(FILE_NAME, 2, 2)
