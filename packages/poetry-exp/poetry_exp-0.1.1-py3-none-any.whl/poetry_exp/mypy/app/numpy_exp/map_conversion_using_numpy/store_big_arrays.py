import math
import numpy as np
import time

MAP_FILE = 'blockinfo'
#BIT_MAP_FILE = '100GbBinaryBitmap'  # 62.5 MB this is taking more space than textBitmap(31.2 MB)
BIT_MAP_FILE = 'bigFile.npz'  # 6.25 MB this is taking more space than textBitmap(3.12 MB)

volume_block_size = 65536  # Bytes  (64 KB)
volume_length = 107374182400  # Bytes  (100 GB)
volume_length = 42949672960  # Bytes (40 GB)
volume_length = 5 * 1024 * 1024 * 1024  # Bytes (5 GB)
volume_length = 1073741824  # Bytes (1 GB) # took 15 sec to write, takes 1.22 MB space

#volume_length = 100  # Bytes  (1000 GB)
BATCH_SIZE = 1000000

def get_arr(index):
    return "arr_" + str(index)

def convert_map():
    chunks = math.ceil(volume_length/BATCH_SIZE)
    #chunks_arr = {i: "arr_"+str(i) for i in range(chunks)}
    print(f'chunks: {chunks}')
    with open(BIT_MAP_FILE, 'wb') as f:
        for i in range(chunks):
           map = np.zeros(BATCH_SIZE, dtype=np.uint8)
           #print(map)
           #np.savetxt(f, [map], fmt='%d')
           array_name = "arr_"+str(i)
           save_info = {array_name: map}
           np.savez_compressed(f, **save_info)

    # #print(f'map: {map}')
    # with open(MAP_FILE) as map_fp:
    #     cbt_map = map_fp.read()
    #     if cbt_map:
    #         cbt_map_blocks = cbt_map.split()
    #         for change_block in cbt_map_blocks:
    #             change_block_arr = change_block.split(',')
    #             vmware_offset = int(change_block_arr[0])  # In bytes
    #             vmware_length = int(change_block_arr[1])  # in Bytes
    #             print(f'vmware_offset: {vmware_offset}, vmware_length: {vmware_length}')
    #
    #             # round up to upper value
    #             block_counts = vmware_length  # number of blocks to read
    #             start = vmware_offset  # round up to lower value
    #
    #             print(f'block_counts: {block_counts}, start from : {start}')
    #             i = 0
    #             while block_counts > 0:
    #                 map[start + i] = 1
    #                 block_counts -= 1
    #                 i += 1
    #
    # #np.save(BIT_MAP_FILE, map)
    # np.savez_compressed(BIT_MAP_FILE, map)


if __name__ == '__main__':
    t1 = time.time()

    #convert_map()

    #bitmap = np.load(BIT_MAP_FILE + ".npy")[1:5]
    #bitmap = np.loadtxt(BIT_MAP_FILE, dtype=np.uint8)["arr_0"][1:5]
    #bitmap = np.load(BIT_MAP_FILE)["arr_0"][1:5]
    bitmap = np.load(BIT_MAP_FILE)['arr_1074']
    print(bitmap)
    # for b in bitmap:
    #     print(type(b))

    # print(len(bitmap))
    # print(bitmap)

    # bitmap = np.load(BIT_MAP_FILE)["arr_1"]
    # print(bitmap)
    #print(bitmap)
    t2 = time.time()
    print(f'Time taken: {t2-t1}')  # 1 sec for 1000 GB, 0.5 sec for 100 GB
    #print(''.join([str(i) for i in bitmap]))
