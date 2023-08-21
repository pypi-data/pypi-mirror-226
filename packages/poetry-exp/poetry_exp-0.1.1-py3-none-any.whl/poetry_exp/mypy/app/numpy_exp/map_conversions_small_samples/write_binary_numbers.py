newFileBytes = [1, 1, 0, 0, 1, 0, 0, 0, 1, 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
# make file
newFile = open("binarymap.txt", "wb")
# write to file
for byte in newFileBytes:
    newFile.write(byte.to_bytes(1, byteorder='big'))