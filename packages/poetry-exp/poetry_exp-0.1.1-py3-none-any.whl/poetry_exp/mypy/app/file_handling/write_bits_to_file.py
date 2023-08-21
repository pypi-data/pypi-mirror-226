import struct


def write_bits(bits_str):
    print(f'Size of bits: {len(bits_str)}')
    i = 0
    buffer = bytearray()
    while i < len(bits_str):
        buffer.append(int(bits_str[i:i + 8], 2))
        i += 8
    # now write your buffer to a file
    with open("test.bin", 'bw') as f:
        f.write(buffer)


if __name__ == '__main__':
    bits = "1010101010101010"

    write_bits(bits)