
file_name = 'blockinfo'
block_size = 4096  # 4k
VVMAP_BITS_PER_BYTE = 8


def decimal_to_binary(num):
    return bin(num).replace("0b", "")
# e.g
# e.g decimal_to_binary(240)  # '11110000'
# e.g binary_to_decimal(2)  # 10


def binary_to_decimal(bin_str):
    return int(bin_str, 2)

# e.g binary_to_decimal('11110000')  # 240
# e.g binary_to_decimal('10')  # 2


def binary_to_hex(bin_str):
    return hex(binary_to_decimal(bin_str))
# binary_to_hex('1110')  # 0xe

def get_offset_in_bytes(offset):
    return offset / VVMAP_BITS_PER_BYTE


def get_first_byte_mask(start):
    return (~0) << (start & VVMAP_BITS_PER_BYTE - 1)


def get_last_byte_mask(size):
    return (~0) >> (-size & (VVMAP_BITS_PER_BYTE - 1))


def generate_bit_map(fp, start, length):
    size = start + length
    total_bits = VVMAP_BITS_PER_BYTE - (start % VVMAP_BITS_PER_BYTE)
    byte_mask = get_first_byte_mask(start)
    print(f'byte_mask: {byte_mask}')

    while length - total_bits >= 0:
        fp.write(bytes(byte_mask))
        length -= total_bits
        total_bits = VVMAP_BITS_PER_BYTE
        byte_mask = ~0

    if length:
        byte_mask &= get_last_byte_mask(size)
        print(f'Inside len, byte_mask: {byte_mask}')


def generate_map(fp, start, length):
    size = start + length
    total_bits = VVMAP_BITS_PER_BYTE - (start % VVMAP_BITS_PER_BYTE)
    byte_mask = get_first_byte_mask(start)
    print(f'byte_mask: {byte_mask}')

    while length - total_bits >= 0:
        fp.write(bytes(byte_mask))
        length -= total_bits
        total_bits = VVMAP_BITS_PER_BYTE
        byte_mask = ~0

    if length:
        byte_mask &= get_last_byte_mask(size)
        print(f'Inside len, byte_mask: {byte_mask}')

def convert_map():
    with open(file_name) as map_fp:
        cbt_map = map_fp.read()
        if cbt_map:
            cbt_map_blocks = cbt_map.split()
            with open('transformed_map', 'wb') as trans_map_fp:
                for change_block in cbt_map_blocks:
                    change_block_arr = change_block.split(',')
                    vmware_offset = int(change_block_arr[0])
                    vmware_length = int(change_block_arr[1])
                    offset = vmware_offset // block_size
                    length = vmware_length // block_size
                    print(f'offset: {offset}, length: {length}')
                    #print(f'offset: {type(offset)}, length: {type(length)}')
                    generate_bit_map(trans_map_fp, offset, length)
                    #print(f'...........{cbt_map_blocks}')



if __name__ == '__main__':
    convert_map()