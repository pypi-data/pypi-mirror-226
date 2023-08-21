    #include <stdlib.h>
    #include <errno.h>
    #include <stdio.h>
    #include <inttypes.h>
    #include <string.h>
    #include <stdarg.h>
    #include <fcntl.h>
    #include <unistd.h>
    #include <iostream>
    #include <bits/stdc++.h>
    using namespace std;
   
    /*
      This is how the blockinfo looks from vmware
        0,65536   //Offset, length in bytes
        1048576,525402112
        2673868800,18756927488
        21474770944,65536
    */

    //uint8_t *catalystbuffer = (uint8_t *)malloc(2);
    /*
     char *buffer = malloc(255);
     char *token;
     FILE *fp = NULL;
     uint64_t blockSize  = volumeBlockSize; // This is block size passed
     uint64_t map_length = (volumeLength/blockSize)/VVMAP_BITS_PER_BYTE; //volumeLength is total disk size
     uint64_t vmware_offset = 0;
     uint64_t vmware_length = 0;
     while(fgets(buffer, 255, (FILE*) fp)) {
        token = strtok(buffer, s);
        vmware_offset = (uint64_t)atoll(token);
        token = strtok(NULL, s);
        vmware_length = (uint64_t)atoll(token);
        VVMAP_LOG_DEBUG(pLogContext, "DEBASISH OFFSET %" PRIu64 " and LENGTH %" PRIu64" ",
                        vmware_offset, vmware_length);

        unsigned int start = vmware_offset/blockSize;
        int length =  vmware_length/blockSize;
        setBitMapBuffer(location, start, length);
     }
    */
    #define VVMAP_BITS_PER_BYTE 8

    #define OFFSET_IN_BYTES(offset)    ((offset) / VVMAP_BITS_PER_BYTE) //Offset within the byte array
    //((uint8_t)(~0U) is all 1's
    #define FIRST_BYTE_MASK(start) (((uint8_t)(~0U)) << ((start) & (VVMAP_BITS_PER_BYTE - 1)))
    //-(size) is 2's complement of size
    #define LAST_BYTE_MASK(size) (((uint8_t)(~0U)) >> (-(size) & (VVMAP_BITS_PER_BYTE - 1)))

    uint8_t catalystbuffer[32];
    void setBitMapBuffer(uint8_t *map, unsigned int start, int len)
    {
        //Move the *map pointer with in the array 
        uint8_t *p = map + OFFSET_IN_BYTES(start);
        // How many total Bits you needs to set within the *map, that is your size
        const unsigned int size = start + len;
        //How many total number of bits needs to be set  within a byte
        int total_bits = VVMAP_BITS_PER_BYTE - (start % VVMAP_BITS_PER_BYTE);

        //Calcualte start byte index mask
        uint8_t byte_mask = FIRST_BYTE_MASK(start);

        //Loops untill the last BYTE index, if there are 4 bytes, loop over 3 bytes first
        while (len - total_bits >= 0) {
          //from start first byte is set 
          *p |= byte_mask;
          //length will skeep to next byte 
          //total_bits is reset to 8
          //byte_mask is all 1's , as subsequent Byte blocks are all set to 1 untill last block
          len -= total_bits;
          total_bits = VVMAP_BITS_PER_BYTE;
          byte_mask = ~0;
          p++; //Move to next Byte index
        }
        //For the last byte index 
        if (len) {
          //Calcualte last byte index mask, once (len - total_bits < 0) exits above while loop
          byte_mask &= LAST_BYTE_MASK(size);
          *p |= byte_mask;
        }
    }

   int main () {
      //memset(catalystbuffer, 0, 2);
      // Following arguments are hardcoded for demo purpose 
      // Set first 2 bytes to zero
      catalystbuffer[0] = 0;
      catalystbuffer[1] = 0;
      catalystbuffer[2]|= ((3) & (VVMAP_BITS_PER_BYTE - 1));
      catalystbuffer[3]|= FIRST_BYTE_MASK(3);
      catalystbuffer[4]|= (-(5) & (VVMAP_BITS_PER_BYTE - 1));
      catalystbuffer[5]|= LAST_BYTE_MASK(5);
      /*
      Actual bit representation
      0       0       0       1       1       0       0       0 //setBitMapBuffer() result

      0       0       0       0       0       0       0       0

      0       0       0       0       0       0       1       1 //((3) & (VVMAP_BITS_PER_BYTE - 1)); value is 3

      1       1       1       1       1       0       0       0 //FIRST_BYTE_MASK; left shift by 3

      0       0       0       0       0       0       1       1 //(-(5) & (VVMAP_BITS_PER_BYTE - 1)); value is 3

      0       0       0       1       1       1       1       1 //LAST_BYTE_MASK; Right shift by 3

      0       0       0       0       0       0       0       0

      0       0       0       0       0       0       0       0

      */

      // Set from 3rd bit to length 2
      setBitMapBuffer(catalystbuffer, 3, 2);
      //For Printing the array
      int j = 0;
      int k = 0;
      for(; k<8; k++){
        uint8_t char_to_print = catalystbuffer[k];
        for (; j<8; j++){
          std::cout << "" << (char_to_print &  0X01)<<'\t';
           // printf("\n");
          // printf("%i\n", test & 0X01);
          char_to_print = char_to_print >> 1;
        }
        j = 0;
        printf("\n\n");
      }

      return 0;
    }
